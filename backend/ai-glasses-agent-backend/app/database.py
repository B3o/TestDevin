from datetime import datetime
from typing import Dict, List, Optional
from .models import FoodItem, NavigationAlert, User

# In-memory database
class Database:
    def __init__(self):
        self.users: Dict[str, User] = {}  # email -> user
        self.next_user_id: int = 1
        self.food_items: Dict[str, List[FoodItem]] = {}  # user_id -> food items
        self.navigation_history: Dict[str, List[NavigationAlert]] = {}  # user_id -> navigation alerts

    def add_food_item(self, user_id: str, food_item: FoodItem):
        if user_id not in self.food_items:
            self.food_items[user_id] = []
        self.food_items[user_id].append(food_item)
    
    def get_food_items(self, user_id: str) -> List[FoodItem]:
        return self.food_items.get(user_id, [])

    def add_navigation_alert(self, user_id: str, alert: NavigationAlert):
        if user_id not in self.navigation_history:
            self.navigation_history[user_id] = []
        self.navigation_history[user_id].append(alert)
    
    def get_navigation_history(self, user_id: str) -> List[NavigationAlert]:
        return self.navigation_history.get(user_id, [])
    
    def add_user(self, email: str, password_hash: str, name: Optional[str] = None) -> User:
        if email in self.users:
            raise ValueError("Email already exists")
        
        user = User(
            id=self.next_user_id,
            email=email,
            password_hash=password_hash,
            name=name,
            created_at=datetime.now()
        )
        self.users[email] = user
        self.next_user_id += 1
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.users.get(email)
    
    def update_last_login(self, email: str) -> None:
        if email in self.users:
            self.users[email].last_login = datetime.now()

# Global database instance
db = Database()
