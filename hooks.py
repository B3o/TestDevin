from typing import Callable, Dict, List, Any, Optional
from functools import wraps
from common.log import logger

class HookManager:
    """Hook management system for Image2Video plugin"""
    
    def __init__(self):
        self._hooks: Dict[str, List[Callable]] = {
            "before_image_upload": [],
            "after_image_upload": [],
            "before_video_generation": [],
            "after_video_generation": [],
        }
    
    def register_hook(self, hook_name: str, func: Callable) -> Callable:
        """Register a hook function for a specific event"""
        if hook_name in self._hooks:
            logger.info(f"Registering hook {func.__name__} for event {hook_name}")
            self._hooks[hook_name].append(func)
        return func
    
    def run_hooks(self, hook_name: str, **kwargs) -> None:
        """Execute all registered hooks for a specific event"""
        if hook_name in self._hooks:
            logger.info(f"Running hooks for event {hook_name}")
            for func in self._hooks[hook_name]:
                try:
                    func(**kwargs)
                except Exception as e:
                    logger.error(f"Error running hook {func.__name__}: {str(e)}")

# Global hook manager instance
hook_manager = HookManager()

def register_hook(hook_name: str):
    """Decorator for registering hook functions"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return hook_manager.register_hook(hook_name, wrapper)
    return decorator

# Example usage:
"""
@register_hook("before_image_upload")
def log_image_upload(image_data: bytes, **kwargs):
    logger.info(f"About to upload image of size {len(image_data)} bytes")

# Later in the code:
hook_manager.run_hooks("before_image_upload", image_data=image_bytes)
"""
