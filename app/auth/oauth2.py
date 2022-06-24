from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.auth.jwt_token import verify_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentails_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentails_exception)
