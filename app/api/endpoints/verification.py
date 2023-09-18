from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.api.deps import get_current_active_user
from app.core.deps import get_session
from app.core.security import generate_and_send_verification_code, check_is_staff
from app.models.user import User
import datetime



router = APIRouter()
@router.post("/users/verify_code", dependencies=[Depends(get_current_active_user)])
def verify_code(*, session: Session = Depends(get_session),
                code: str,
                current_user=None):
    if current_user is None:
        current_user = Depends(get_current_active_user)
    current_time = datetime.datetime.now()
    expiry_date = current_user.code_expiration_time

    if current_user.verification_code == code and current_time < expiry_date:
        current_user.is_verified = True
        if check_is_staff(current_user.email):
            current_user.is_staff = True
        session.commit()

    elif current_user.verification_code != code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code"
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code has expired"
        )

    return {"message": "Verification complete"}


@router.post("/users/send_verification_code")
async def send_verification_code(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    await generate_and_send_verification_code(session, current_user)
    return {"message": "Verification code generated and sent via email"}