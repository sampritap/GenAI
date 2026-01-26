"""
DAY 5 - TASK 2: JWT Authentication Advanced

Theory:
- Refresh tokens (long-lived)
- Access tokens (short-lived)
- Token refresh endpoint
- Role-based access control
- Token in database
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from enum import Enum

# ============================================
# CONFIGURATION
# ============================================

SECRET_KEY = "your-secret-key-for-access-tokens"
REFRESH_SECRET_KEY = "your-secret-key-for-refresh-tokens"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Short-lived
REFRESH_TOKEN_EXPIRE_DAYS = 7     # Long-lived

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

app = FastAPI()

# ============================================
# ENUMS AND MODELS
# ============================================

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class User(BaseModel):
    username: str
    email: str
    role: UserRole
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRequest(BaseModel):
    refresh_token: str

# ============================================
# SIMULATED DATABASE
# ============================================

fake_users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "role": UserRole.ADMIN,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lm",  # secret
        "disabled": False,
    },
    "john": {
        "username": "john",
        "email": "john@example.com",
        "role": UserRole.USER,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lm",  # secret
        "disabled": False,
    },
    "guest": {
        "username": "guest",
        "email": "guest@example.com",
        "role": UserRole.GUEST,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lm",  # secret
        "disabled": False,
    }
}

# Simulated token blacklist
token_blacklist = set()

# ============================================
# UTILITY FUNCTIONS
# ============================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticate user"""
    if username not in fake_users_db:
        return None
    user = fake_users_db[username]
    if not verify_password(password, user["hashed_password"]):
        return None
    return UserInDB(**user)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create short-lived access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create long-lived refresh token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)) -> User:
    """Verify access token and get current user"""
    token = credentials.credentials
    
    if token in token_blacklist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    if username not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    user = fake_users_db[username]
    return User(**user)

async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency: User must be admin"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user

# ============================================
# ENDPOINTS
# ============================================

@app.post("/login")
async def login(username: str, password: str) -> Token:
    """
    Login - returns both access and refresh tokens
    
    Test:
        curl -X POST "http://localhost:8000/login?username=admin&password=secret"
    """
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
        )
    
    # Create both tokens
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/refresh")
async def refresh_access_token(token_request: TokenRequest) -> Token:
    """
    Refresh access token using refresh token
    
    Test:
        curl -X POST "http://localhost:8000/refresh" \\
             -H "Content-Type: application/json" \\
             -d '{"refresh_token": "<your_refresh_token>"}'
    """
    try:
        payload = jwt.decode(
            token_request.refresh_token,
            REFRESH_SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    # Create new access token
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "refresh_token": token_request.refresh_token,
        "token_type": "bearer"
    }

@app.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)) -> User:
    """Get current user info - requires valid access token"""
    return current_user

@app.post("/logout")
async def logout(current_user: User = Depends(get_current_user)) -> dict:
    """
    Logout - add token to blacklist
    In production, store in Redis for efficiency
    """
    # In real app, extract token from header and add to blacklist
    return {"message": f"User {current_user.username} logged out"}

@app.get("/admin-only")
async def admin_endpoint(admin_user: User = Depends(require_admin)) -> dict:
    """
    Admin only endpoint
    
    Test:
        curl -H "Authorization: Bearer <admin_token>" http://localhost:8000/admin-only
    """
    return {
        "message": "Welcome admin!",
        "admin": admin_user.username,
        "role": admin_user.role
    }

@app.get("/users")
async def list_users(current_user: User = Depends(get_current_user)) -> dict:
    """
    List all users - requires authentication
    Only admins can see this in real apps
    """
    users = [
        {"username": u["username"], "role": u["role"]}
        for u in fake_users_db.values()
    ]
    return {
        "requested_by": current_user.username,
        "users": users
    }

# ============================================
# HOW TO RUN AND TEST
# ============================================

"""
Run the server:
    uvicorn learning_tasks.auth.task_2_jwt_advanced:app --reload

Test Credentials:
- admin / secret (ADMIN role)
- john / secret (USER role)
- guest / secret (GUEST role)

Test Flow:

1. Login as admin:
    curl -X POST "http://localhost:8000/login?username=admin&password=secret"
    
    Response:
    {
        "access_token": "...",
        "refresh_token": "...",
        "token_type": "bearer"
    }

2. Use access token to access protected endpoint:
    curl -H "Authorization: Bearer <access_token>" http://localhost:8000/me

3. Access admin-only endpoint:
    curl -H "Authorization: Bearer <access_token>" http://localhost:8000/admin-only

4. Try to access as non-admin (fails):
    curl -X POST "http://localhost:8000/login?username=john&password=secret"
    curl -H "Authorization: Bearer <user_token>" http://localhost:8000/admin-only
    # 403 Forbidden

5. Refresh access token:
    curl -X POST "http://localhost:8000/refresh" \\
         -H "Content-Type: application/json" \\
         -d '{"refresh_token": "<refresh_token>"}'

6. Logout:
    curl -X POST -H "Authorization: Bearer <access_token>" http://localhost:8000/logout

Key Differences from Task 1:
- Two tokens: access (short-lived) + refresh (long-lived)
- Admin role check dependency
- Token blacklist for logout
- Token type validation (access vs refresh)
"""
