import secrets
import jwt
import hmac
import hashlib
from datetime import datetime, timezone, timedelta
from pwdlib import PasswordHash
from config import settings
from exceptions.authentication_exception import AccessTokenExpiredException, InvalidAccessTokenException, InvalidRefreshTokenException, RefreshTokenExpiredException

SECRET_KEY = settings.secret_key
ALGORITHM = 'HS256'

def get_password_hash(password: str):
    password_hash = PasswordHash.recommended()
    return password_hash.hash(password)

def hash_email(email: str) -> str:
    normalized_email = email.strip().lower()
    return hmac.new(
        key=settings.email_hash_secret.encode("utf-8"),
        msg=normalized_email.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()
    
def generate_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"

def verify_otp_code(stored_code: str, input_code: str) -> bool:
    return hmac.compare_digest(stored_code, input_code.strip())

def verify_password(password: str, hash_key: str):
    password_hash = PasswordHash.recommended()
    return password_hash.verify(password, hash_key)

def create_token(token_data: dict, expires_time_minutes, token_type: str):
    payload = token_data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_time_minutes)
    payload.update({'exp': expire, 'type': token_type})
    encode_jwt = jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)
    return encode_jwt
    
def _decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def decode_access_token(access_token: str):
    try:
        payload = _decode_token(access_token)
    except jwt.ExpiredSignatureError:
        raise AccessTokenExpiredException()
    except jwt.InvalidTokenError:
        raise InvalidAccessTokenException()
    return payload
    
def decode_refresh_token(refresh_token: str):
    try:
        payload = _decode_token(refresh_token)
    except jwt.ExpiredSignatureError:
        raise RefreshTokenExpiredException()
    except jwt.InvalidTokenError:
        raise InvalidRefreshTokenException()
    return payload