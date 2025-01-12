from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: int
    email: EmailStr
    password_hash: str
    name: Optional[str] = None
    created_at: datetime = datetime.now()
    last_login: Optional[datetime] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class AuthResponse(BaseModel):
    user_id: int
    email: str
    name: Optional[str] = None
    token: str

class TranslationRequest(BaseModel):
    image_url: str  # Base64 encoded image data
    source_language: str = "auto"
    target_language: str
    coordinates: Optional[dict] = None  # x, y coordinates for point-and-translate

class TranslationResponse(BaseModel):
    translated_text: str
    original_text: str
    confidence: float

class FoodTrackRequest(BaseModel):
    image: str

class FoodItem(BaseModel):
    name: str
    calories: float
    timestamp: datetime
    image_url: str

class NavigationAlert(BaseModel):
    alert_type: str  # obstacle, landmark, warning
    description: str
    distance: Optional[float]
    direction: Optional[str]
