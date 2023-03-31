import random
import string
import os

import bcrypt

import jwt

from dotenv import load_dotenv


load_dotenv()


def hash_password(password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def generate_otp(N=4):
    # Generate a string of length N consisting of digits
    return ''.join(random.choices(string.digits, k=N))


def verify_password(password: str, hashed_password: bytes):
    # Check hashed password. Using bcrypt,
    # the salt is saved into the hash itself
    password = password.encode('utf-8')

    return bcrypt.checkpw(password, hashed_password)


def verify_otp(otp: str, hashed_otp: bytes):
    # Check hashed OTP. Using bcrypt,
    # the salt is saved into the hash itself
    otp = otp.encode('utf-8')

    return bcrypt.checkpw(otp, hashed_otp)


def hash_otp(otp: str):
    # Hash an OTP for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(otp.encode('utf-8'), bcrypt.gensalt())


def generate_token(data: dict):
    # Generate a JWT token from a dictionary
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

    return jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_jwt_token(tok: str):
    # decode a JWT token

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

    return jwt.decode(tok, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
