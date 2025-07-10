import uuid

from fastapi import APIRouter
from fastapi.params import Header

from app.db.user.crud import get_user_by_email_and_password, insert_user, update_user, verify_token
from app.models.user import SignupRequest, LoginRequest
from app.utils.api_utils import error_response, success_response

router = APIRouter()

@router.post("/signup")
async def signup(signup_request: SignupRequest):
    existing_user = get_user_by_email_and_password(signup_request.email, signup_request.password)
    if existing_user:
        return error_response("User already exists", {"email": signup_request.email})
    user_id = insert_user(signup_request.name, signup_request.email, signup_request.password)
    return success_response("User created successfully", {"user_id": user_id})


@router.post("/login")
async def login(login_request: LoginRequest):
    user = get_user_by_email_and_password(login_request.email, login_request.password)
    if user and not user.get("is_blocked", False) and user.get("is_active", True):
        token = str(uuid.uuid4())
        update_user(user["id"], token)
        # User found and is active
        return success_response("Login successful",
                                {"user_id": str(user["id"]), "token": token, "name": user.get("name", "")})
    elif user and user.get("is_blocked", False):
        return error_response("User is blocked", None)
    elif user and not user.get("is_active", True):
        return error_response("User is not active", None)
    else:
        return error_response("Invalid email or password", None)

# verify token of user give 200 or 400
@router.get("/verifyToken")
async def verify_token_api(token=Header(None)):
    user = verify_token(token)
    if user:
        return success_response("Token is valid", None)
    else:
        return error_response("Invalid or expired token", None)