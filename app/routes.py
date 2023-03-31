from typing import List

from fastapi import APIRouter, Path, Query, WebSocket, Depends

from app.dependencies import get_user_id

from app.forms import (
    RequestAidForm,
    RegisterForm,
    UpdateAccountForm,
    LoginForm,
    ResetPasswordForm
)

from app.models import (
    Request
)

import app.controllers as controllers


router = APIRouter()

active_ws_connections: List[WebSocket] = []


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.post("/request-aid")
async def request_aid(
    body: RequestAidForm,
    user_id: str = Depends(get_user_id)
):

    data = {"user_id": user_id, **body.dict()}

    result = controllers.post_request(**data)

    if result['success']:
        await _broadcast_message({
            'id': result['id'],
            **data
        })

    return result


@router.get("/requests/{request_id}", response_model=Request)
async def get_request(request_id: str = Path()):

    return controllers.get_request(request_id)


@router.get("/requests", response_model=List[Request])
async def get_requests(
    status: str = Query(None),
    user_id: str = Query(None)
):

    return controllers.get_requests(status, user_id)


# AUth Routes

@router.post("/register")
def register(body: RegisterForm):

    return controllers.register_user(**body.dict())


@router.post("/login")
async def login(body: LoginForm):

    return controllers.login_user(**body.dict())


@router.put("/reset-password")
def reset_password(body: ResetPasswordForm):

    return controllers.reset_password(**body.dict())


@router.get("/otp")
def send_otp(email: str = Query()):

    return controllers.send_otp(email)


@router.put("/update-account")
async def update_account(
    body: UpdateAccountForm,
    user_id: str = Depends(get_user_id)
):

    return controllers.update_user(
        user_id,
        body.dict(exclude_none=True)
    )


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        active_ws_connections.append(websocket)
        data = websocket.receive_json()
        await websocket.send_text("Message Received!")

        print(data)


async def _broadcast_message(message: str):
    for connection in active_ws_connections:
        await connection.send_json(message)
