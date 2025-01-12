from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from typing import Optional, Dict, Any
import bcrypt
import jwt
import os
from typing import Optional
from deep_translator import GoogleTranslator
from .models import (
    TranslationRequest, TranslationResponse, FoodItem, NavigationAlert, FoodTrackRequest,
    User, LoginRequest, RegisterRequest, AuthResponse
)
from .database import db

# Authentication configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        if user_id is None or email is None:
            raise HTTPException(
                status_code=401,
                detail=get_error_message("invalid_token", "en")
            )
        return {"user_id": user_id, "email": email}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail=get_error_message("token_expired", "en")
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail=get_error_message("invalid_token", "en")
        )

# Error messages
ERROR_MESSAGES = {
    "en": {
        "email_exists": "Email is already registered",
        "invalid_credentials": "Invalid email or password",
        "user_not_found": "User not found",
        "invalid_token": "Invalid authentication token",
        "token_expired": "Authentication token has expired",
        "missing_token": "Authentication token is missing",
    },
    "zh": {
        "email_exists": "该邮箱已被注册",
        "invalid_credentials": "邮箱或密码无效",
        "user_not_found": "用户不存在",
        "invalid_token": "无效的认证令牌",
        "token_expired": "认证令牌已过期",
        "missing_token": "缺少认证令牌",
    }
}
import base64
from PIL import Image
import io

app = FastAPI()

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

def get_error_message(key: str, lang: str = "en") -> str:
    return ERROR_MESSAGES.get(lang, ERROR_MESSAGES["en"]).get(key, ERROR_MESSAGES["en"][key])

@app.post("/api/auth/register", response_model=AuthResponse)
async def register(request: RegisterRequest, req: Request):
    # Check if user exists
    if db.get_user_by_email(request.email):
        lang = req.headers.get("accept-language", "en").split(",")[0].lower()
        raise HTTPException(
            status_code=400,
            detail=get_error_message("email_exists", lang)
        )
    
    # Hash password
    password_bytes = request.password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    
    # Create user
    try:
        user = db.add_user(
            email=request.email,
            password_hash=hashed_password.decode('utf-8'),
            name=request.name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Generate token
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow().timestamp() + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return AuthResponse(
        user_id=user.id,
        email=user.email,
        name=user.name,
        token=token
    )

@app.post("/api/auth/login", response_model=AuthResponse)
async def login(request: LoginRequest, req: Request):
    # Get user
    user = db.get_user_by_email(request.email)
    if not user:
        lang = req.headers.get("accept-language", "en").split(",")[0].lower()
        raise HTTPException(
            status_code=401,
            detail=get_error_message("invalid_credentials", lang)
        )
    
    # Verify password
    if not bcrypt.checkpw(
        request.password.encode('utf-8'),
        user.password_hash.encode('utf-8')
    ):
        lang = req.headers.get("accept-language", "en").split(",")[0].lower()
        raise HTTPException(
            status_code=401,
            detail=get_error_message("invalid_credentials", lang)
        )
    
    # Update last login
    db.update_last_login(request.email)
    
    # Generate token
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow().timestamp() + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return AuthResponse(
        user_id=user.id,
        email=user.email,
        name=user.name,
        token=token
    )

@app.post("/api/auth/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # In a real implementation, we might want to blacklist the token
    # For now, just return success as the frontend will remove the token
    return {"status": "success"}

@app.post("/api/translate", response_model=TranslationResponse)
async def translate_image(request: TranslationRequest):
    try:
        # Input validation
        if not request.image_url:
            print("Error: Missing image data")
            raise HTTPException(status_code=400, detail="Image data is required")
            
        # Extract base64 data
        try:
            image_data = request.image_url
            if "base64," in image_data:
                # Split on first occurrence of base64,
                image_data = image_data.split("base64,", 1)[1]
            
            # Validate base64 format
            try:
                image_bytes = base64.b64decode(image_data)
                print("Successfully decoded base64 image data")
            except Exception as e:
                print(f"Base64 decode error: {str(e)}")
                raise HTTPException(status_code=400, detail="Invalid image format")
                
            # Validate image data
            try:
                image = Image.open(io.BytesIO(image_bytes))
                print(f"Successfully opened image: {image.format} {image.size}")
            except Exception as e:
                print(f"Image processing error: {str(e)}")
                raise HTTPException(status_code=400, detail="Invalid image data")
                
        except HTTPException:
            raise
        except Exception as e:
            print(f"Image extraction error: {str(e)}")
            raise HTTPException(status_code=400, detail="Failed to process image data")
            
        # Translation
        try:
            # For now, we'll simulate with dummy text
            original_text = "Hello World"
            translator = GoogleTranslator(source='auto', target=request.target_language)
            translated = translator.translate(original_text)
            print(f"Translation successful: {original_text} -> {translated}")
            
            return TranslationResponse(
                translated_text=translated,
                original_text=original_text,
                confidence=0.95
            )
        except Exception as e:
            print(f"Translation service error: {str(e)}")
            raise HTTPException(status_code=500, detail="Translation service error")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in translation endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/food/track")
async def track_food(request: FoodTrackRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    try:
        # Remove data URL prefix if present
        if "base64," in request.image:
            image = request.image.split("base64,")[1]
            
        # Decode base64 image
        try:
            image_data = base64.b64decode(image)
            image_io = io.BytesIO(image_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid base64 image data")
        
        # In a real implementation, we would:
        # 1. Use ML model to identify food
        # 2. Calculate calories
        # For now, we'll simulate with dummy data
        food_item = FoodItem(
            name="Sample Food",
            calories=500.0,
            timestamp=datetime.now(),
            image_url="sample_url"
        )
        
        db.add_food_item(current_user["user_id"], food_item)
        return {"message": "Food tracked successfully", "food_item": food_item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/food/history")
async def get_food_history(current_user: Dict[str, Any] = Depends(get_current_user)):
    try:
        food_items = db.get_food_items(current_user["user_id"])
        return {"food_items": food_items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/navigation/alert")
async def process_navigation(image: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    try:
        # Remove data URL prefix if present
        if "base64," in image:
            image = image.split("base64,")[1]
            
        # Decode base64 image
        try:
            image_data = base64.b64decode(image)
            image_io = io.BytesIO(image_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid base64 image data")
            
        # In a real implementation, we would:
        # 1. Process image using computer vision
        # 2. Detect obstacles and landmarks
        # For now, we'll simulate with different types of alerts
        import random
        alert_types = [
            ("obstacle", "Door ahead", 2.5, "forward"),
            ("warning", "Stairs approaching", 3.0, "forward"),
            ("landmark", "Open space ahead", 5.0, "forward"),
            ("obstacle", "Wall on the right", 1.0, "right")
        ]
        alert_type, desc, dist, direction = random.choice(alert_types)
        
        alert = NavigationAlert(
            alert_type=alert_type,
            description=desc,
            distance=dist,
            direction=direction
        )
        db.add_navigation_alert(current_user["user_id"], alert)
        return {"message": "Navigation alert processed", "alert": alert}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/navigation/history")
async def get_navigation_history(current_user: Dict[str, Any] = Depends(get_current_user)):
    try:
        alerts = db.get_navigation_history(current_user["user_id"])
        return {"alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
