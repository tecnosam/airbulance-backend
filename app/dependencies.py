from fastapi import Header, HTTPException, Depends

from app.utils.security import decode_jwt_token

import jwt.exceptions


def verify_access_token(token: str = Header(...)):

    try:
        user_data = decode_jwt_token(token)

        return user_data

    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_user_id(user_data: dict = Depends(verify_access_token)):

    return user_data['id']
