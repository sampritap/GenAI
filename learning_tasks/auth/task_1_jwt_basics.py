"""
DAY 5 - TASK 1: JWT Authentication Basics

Theory:
- JWT = JSON Web Token (secure token for authentication)
- Structure: Header.Payload.Signature
- Used to verify user identity without storing sessions
- Great for APIs, mobile apps, microservices
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# ============================================
# CONFIGURATION
# ============================================

SECRET_KEY = "your-secret-key-keep-this-secure-change-in-production"  # ⚠️ CHANGE THIS!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()

app = FastAPI()

# ============================================
# DATA MODELS
# ============================================

class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# ============================================
# SIMULATED DATABASE
# ============================================

fake_users_db = {
    "john": {
        "username": "john",
        "full_name": "John Doe",
        "email": "john@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lm",  # password: secret
        "disabled": False,
    }
}

# ============================================
# UTILITY FUNCTIONS
# ============================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticate user by username and password"""
    if username not in fake_users_db:
        return None
    user = fake_users_db[username]
    if not verify_password(password, user["hashed_password"]):
        return None
    return UserInDB(**user)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT token
    
    Args:
        data: Dictionary to encode (usually {"sub": username})
        expires_delta: Token expiration time
    
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)) -> User:
    """
    Verify token and get current user
    Used as a dependency in protected endpoints
    """
    token = credentials.credentials
    
    try:
        # Decode and verify token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token_data = TokenData(username=username)
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if username not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    user = fake_users_db[username]
    return User(**user)

# ============================================
# ENDPOINTS
# ============================================

@app.post("/login")
async def login(username: str, password: str) -> Token:
    """
    Login endpoint - returns JWT token
    
    Test:
        curl -X POST "http://localhost:8000/login?username=john&password=secret"
    """
    # Authenticate user
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    # Create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)) -> User:
    """
    Protected endpoint - requires valid JWT token
    
    Test:
        1. Login first to get token:
           curl -X POST "http://localhost:8000/login?username=john&password=secret"
        
        2. Use token in Authorization header:
           curl -H "Authorization: Bearer <token>" http://localhost:8000/me
    """
    return current_user

@app.get("/info")
async def get_info(current_user: User = Depends(get_current_user)) -> dict:
    """
    Another protected endpoint
    Returns user information
    """
    return {
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "message": f"Hello {current_user.full_name or current_user.username}!"
    }

# ============================================
# PUBLIC ENDPOINT (NO AUTH REQUIRED)
# ============================================

@app.get("/public")
async def public_endpoint() -> dict:
    """Public endpoint - no authentication required"""
    return {"message": "This is public, no token needed"}

# ============================================
# HOW TO RUN AND TEST
# ============================================

"""
Run the server:
    uvicorn learning_tasks.auth.task_1_jwt_basics:app --reload

Test flow:

1. Check public endpoint (no auth):
    curl http://localhost:8000/public

2. Try accessing protected endpoint without token (fails):
    curl http://localhost:8000/me

3. Login to get token:
    curl -X POST "http://localhost:8000/login?username=john&password=secret"
    
    Response:
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
    }

4. Use token to access protected endpoint:
    curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." http://localhost:8000/me

5. Get user info:
    curl -H "Authorization: Bearer <token>" http://localhost:8000/info

Key Concepts:
- LOGIN: Exchange credentials for JWT token
- JWT: Signed token contains user info (payload)
- PROTECTED ENDPOINT: Requires valid JWT in Authorization header
- VERIFY: Server checks JWT signature and expiration
- EXPIRED: Token becomes invalid after ACCESS_TOKEN_EXPIRE_MINUTES

Test Credentials:
- Username: john
- Password: secret
"""
