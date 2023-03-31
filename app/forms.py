from pydantic import BaseModel


class LoginForm(BaseModel):
    email: str
    password: str


class RegisterForm(BaseModel):
    name: str
    email: str
    password: str


class UpdateAccountForm(BaseModel):
    name: str = None
    email: str = None
    password: str = None


class ResetPasswordForm(BaseModel):
    user_id: str
    otp: str
    password: str


class RequestAidForm(BaseModel):
    description: str = None
    location: str
