import os
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from authlib.integrations.starlette_client import OAuth, OAuthError
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from database import get_db
import crud, models

load_dotenv()
router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

COOKIE_NAME = "onefund_token"

def create_token(payload: dict, minutes: int = 60 * 24 * 7):
    to_encode = {"exp": datetime.utcnow() + timedelta(minutes=minutes), **payload}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def read_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = str(request.url_for("google_callback"))
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        prompt="select_account"
    )

@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        body = getattr(getattr(e, "response", None), "text", "")
        raise HTTPException(status_code=400, detail={"error": getattr(e, "error", "oauth_error"), "body": body})

    # Get profile (via discovery userinfo or id_token fallback)
    userinfo = token.get("userinfo")
    if not userinfo:
        userinfo = await oauth.google.parse_id_token(request, token)

    sub = userinfo.get("sub")
    email = userinfo.get("email")
    name = userinfo.get("name")
    picture = userinfo.get("picture")

    if not sub or not email:
        raise HTTPException(status_code=400, detail="Google profile missing sub/email")

    user = crud.get_user_by_google_sub(db, sub) or crud.get_user_by_email(db, email)
    if not user:
        user = crud.create_user(db, sub=sub, email=email, name=name, picture=picture)

    token_str = create_token({"uid": user.id})
    resp = RedirectResponse(url=f"{FRONTEND_URL}/", status_code=HTTP_302_FOUND)
    resp.set_cookie(
        key=COOKIE_NAME,
        value=token_str,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
        path="/",
    )
    return resp

@router.post("/logout")
def logout():
    resp = RedirectResponse(url=f"{FRONTEND_URL}/", status_code=HTTP_302_FOUND)
    resp.delete_cookie(COOKIE_NAME, path="/")
    return resp

def current_user(request: Request, db: Session = Depends(get_db)) -> models.User | None:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    try:
        payload = read_token(token)
        uid = payload.get("uid")
    except JWTError:
        return None
    return db.get(models.User, uid)
