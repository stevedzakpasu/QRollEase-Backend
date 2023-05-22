from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenPayLoad(SQLModel):
    sub: str
