from typing import Optional, Dict, Any, Union, List, Callable
import requests
import json
import os
import time
import base64
import jwt
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bridge.context import ContextType, Context
from bridge.reply import Reply, ReplyType
from common.log import logger
import plugins
from .hooks import HookManager, register_hook
from .lifecycle import Lifecycle, LifecycleState
from .pipeline import Pipeline, PipelineContext

class AppException(Exception):
    pass

@plugins.register(
    name="Image2Video",
    desc="图片生成视频插件",
    version="1.0",
    author="Assistant",
    desire_priority=100,
    hidden=False,
    enabled=True
)
class Image2Video(Lifecycle):
    def __init__(self):
        """Initialize the Image2Video plugin with lifecycle management"""
        super().__init__()
        self.hook_manager = HookManager()
        self.handlers: Dict[str, Callable] = {}
        self.config_data: Optional[Dict[str, Any]] = None
        self.command_prefix: str = "动起来"
        self.session: Optional[requests.Session] = None
        
        # User state management
        self.waiting_for_image: Dict[str, float] = {}   # user_id -> timestamp
        self.waiting_for_prompt: Dict[str, float] = {}  # user_id -> timestamp
        self.user_data: Dict[str, Dict[str, Any]] = {}  # user_id -> session data
        
        # Initialize pipelines
        from .handlers import (
            validate_image_data, upload_image, validate_prompt, 
            generate_video, handle_validation_error, 
            handle_upload_error, handle_generation_error
        )
        
        # Image upload pipeline
        self.upload_pipeline = Pipeline("image_upload")
        self.upload_pipeline.add_step(validate_image_data)
        self.upload_pipeline.add_step(upload_image)
        self.upload_pipeline.add_error_handler(ValueError, handle_validation_error)
        self.upload_pipeline.add_error_handler(Exception, handle_upload_error)
        
        # Video generation pipeline
        self.generation_pipeline = Pipeline("video_generation")
        self.generation_pipeline.add_step(validate_prompt)
        self.generation_pipeline.add_step(generate_video)
        self.generation_pipeline.add_error_handler(ValueError, handle_validation_error)
        self.generation_pipeline.add_error_handler(Exception, handle_generation_error)
        
        # Initialize the plugin
        self.initialize()

    def _do_initialize(self, **kwargs) -> None:
        """Initialize plugin resources and configuration"""
        try:
            # Load configuration
            config_path = os.path.join(os.path.dirname(__file__), "config.json")
            if not os.path.exists(config_path):
                raise FileNotFoundError("Configuration file not found")
                
            with open(config_path, 'r', encoding='utf-8') as file:
                self.config_data = json.load(file)
                
            required_keys = ['api_url', 'imgbb_api_key', 'ak', 'sk']
            missing_keys = [key for key in required_keys if not self.config_data or key not in self.config_data]
            if missing_keys:
                raise ValueError(f"Configuration missing required keys: {', '.join(missing_keys)}")
            
            # Initialize session
            self.session = requests.Session()
            retries = Retry(
                total=3,
                backoff_factor=0.5,
                status_forcelist=[500, 502, 503, 504],
                allowed_methods=["GET", "POST"]
            )
            self.session.mount('http://', HTTPAdapter(max_retries=retries))
            self.session.mount('https://', HTTPAdapter(max_retries=retries))
            
            logger.info("[Image2Video] Configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"[Image2Video] Failed to initialize: {e}")
            raise
            
    def _do_start(self) -> None:
        """Start the plugin processing"""
        if not self.config_data or not self.session:
            raise RuntimeError("Plugin not properly initialized")
            
    def _do_stop(self) -> None:
        """Stop the plugin and cleanup resources"""
        if self.session:
            self.session.close()
            self.session = None
        self.waiting_for_image.clear()
        self.waiting_for_prompt.clear()
        self.user_data.clear()

    def upload_to_imgbb(self, base64_image: str) -> Optional[str]:
        """Upload image to ImgBB and get URL"""
        try:
            # Run pre-upload hooks
            self.hook_manager.run_hooks("before_image_upload", 
                                      base64_image=base64_image)
            
            if not self.config_data:
                raise AppException("Configuration not loaded")
                
            data = {
                'key': self.config_data['imgbb_api_key'],
                'image': base64_image
            }
            
            if not self.session:
                raise RuntimeError("HTTP session not initialized")
                
            response = self.session.post(
                'https://api.imgbb.com/1/upload',
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    # Run post-upload hooks
                    self.hook_manager.run_hooks("after_image_upload", 
                                              image_url=result['data']['url'])
                    return result['data']['url']
                    
            logger.error(f"[Image2Video] Failed to upload to ImgBB: {response.text}")
            return None
            
        except Exception as e:
            logger.error(f"[Image2Video] Failed to upload to ImgBB: {e}")
            return None

    def submit_video_task(self, image_url: str, prompt: str) -> dict:
        """Submit video generation task"""
        try:
            # Run pre-generation hooks
            self.hook_manager.run_hooks("before_video_generation",
                                      image_url=image_url,
                                      prompt=prompt)

            token = self.generate_jwt_token()
            if not token:
                raise Exception("Failed to generate token")

            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            data = {
                "model_name": "kling-v1-6",
                "mode": "pro",
                "duration": "10",
                "image": image_url,
                "prompt": prompt,
                "cfg_scale": 0.8
            }

            if not self.config_data:
                raise AppException("Configuration not loaded")
                
            if not self.session:
                raise RuntimeError("HTTP session not initialized")
                
            response = self.session.post(
                self.config_data['api_url'],
                headers=headers,
                json=data
            )

            if response.status_code != 200:
                raise Exception(f"Failed to submit task: {response.text}")

            result = response.json()
            if result.get('code') != 0:
                raise Exception(f"Failed to submit task: {result.get('message')}")

            # Run post-generation hooks
            self.hook_manager.run_hooks("after_video_generation",
                                      task_id=result['data']['task_id'])

            return result['data']

        except Exception as e:
            logger.error(f"[Image2Video] Failed to submit task: {e}")
            raise

    def generate_jwt_token(self) -> Optional[str]:
        """Generate JWT token"""
        try:
            if not self.config_data:
                raise AppException("Configuration not loaded")

            ak = self.config_data.get('ak')
            sk = self.config_data.get('sk')
            
            if not ak or not sk:
                raise AppException("Missing API credentials (ak/sk)")

            headers = {
                "alg": "HS256",
                "typ": "JWT"
            }
            payload = {
                "iss": ak,
                "exp": int(time.time()) + 1800,  # 30 minutes validity
                "nbf": int(time.time()) - 5
            }
            token = jwt.encode(payload, sk, headers=headers)
            return token
        except Exception as e:
            logger.error(f"[Image2Video] Failed to generate token: {e}")
            return None

    def get_image_data(self, msg: Any, content: str) -> Optional[str]:
        """Extract base64 image data from message"""
        try:
            if hasattr(msg, '_rawmsg') and hasattr(msg._rawmsg, 'download'):
                file_name = msg._rawmsg.get('FileName', 'temp.png')
                temp_path = os.path.join(os.getcwd(), 'tmp', file_name)
                msg._rawmsg.download(temp_path)
                
                if os.path.exists(temp_path):
                    with open(temp_path, 'rb') as f:
                        image_data = f.read()
                    try:
                        os.remove(temp_path)
                    except:
                        pass
                    return base64.b64encode(image_data).decode('utf-8')
            
            if hasattr(msg, '_rawmsg') and 'Content' in msg._rawmsg:
                content_data = msg._rawmsg['Content']
                if isinstance(content_data, str) and len(content_data) > 0:
                    try:
                        image_data = base64.b64decode(content_data)
                        return base64.b64encode(image_data).decode('utf-8')
                    except:
                        pass
            
            return None
            
        except Exception as e:
            logger.error(f"[Image2Video] Failed to get image data: {e}")
            return None

    def on_handle_context(self, e_context: Dict[str, Any]) -> None:
        """Handle user messages and manage the image-to-video workflow
        
        This method requires the plugin to be in STARTED state and properly configured.
        """
        if self.state != LifecycleState.STARTED:
            raise RuntimeError("Plugin must be started before handling context")
        if not self.config_data:
            raise AppException("Plugin not properly configured")

        content = e_context['context'].content
        msg = e_context['context']['msg']
        user_id = msg.from_user_id

        if not user_id:
            return

        try:
            # Check for timeouts
            current_time = time.time()
            if user_id in self.waiting_for_image and (current_time - self.waiting_for_image[user_id]) > 180:
                del self.waiting_for_image[user_id]
                e_context['reply'] = Reply(ReplyType.ERROR, "Operation timed out. Please start over with '动起来'.")
                return
                
            if user_id in self.waiting_for_prompt and (current_time - self.waiting_for_prompt[user_id]) > 180:
                del self.waiting_for_prompt[user_id]
                if user_id in self.user_data:
                    del self.user_data[user_id]
                e_context['reply'] = Reply(ReplyType.ERROR, "Operation timed out. Please start over with '动起来'.")
                return

            # Handle "动起来" command
            if content.startswith(self.command_prefix):
                self.waiting_for_image[user_id] = time.time()
                e_context['reply'] = Reply(ReplyType.TEXT, "Please send the image you want to animate within 3 minutes")
                return

            # Handle image upload using pipeline
            if user_id in self.waiting_for_image:
                # Verify message type is image
                if e_context['context'].type != ContextType.IMAGE:
                    e_context['reply'] = Reply(ReplyType.ERROR, "Please send an image file")
                    return
                    
                # Get image data from message
                image_data = self.get_image_data(msg, content)
                if not image_data:
                    e_context['reply'] = Reply(ReplyType.ERROR, "Failed to get image data. Please try again.")
                    return
                    
                # Run image upload pipeline
                result = self.upload_pipeline.run({
                    'plugin': self,
                    'image_data': image_data,
                    'user_id': user_id
                })
                
                if result.errors:
                    e_context['reply'] = Reply(ReplyType.ERROR, 
                                                    result.metadata.get('error_message', "Failed to process image"))
                    return
                    
                # Store image URL and update state
                image_url = result.data.get('image_url')
                if image_url:
                    self.user_data[user_id] = {'image_url': image_url}
                    del self.waiting_for_image[user_id]
                    self.waiting_for_prompt[user_id] = time.time()
                    e_context['reply'] = Reply(ReplyType.TEXT, "Please enter your desired animation effect description")
                return

            # Handle prompt input using pipeline
            if user_id in self.waiting_for_prompt:
                # Get stored image URL
                user_data = self.user_data.get(user_id, {})
                image_url = user_data.get('image_url')
                if not image_url:
                    e_context['reply'] = Reply(ReplyType.ERROR, "Image data not found. Please start over.")
                    return
                    
                # Run video generation pipeline
                result = self.generation_pipeline.run({
                    'plugin': self,
                    'image_url': image_url,
                    'prompt': content,
                    'user_id': user_id
                })
                
                if result.errors:
                    e_context['reply'] = Reply(ReplyType.ERROR,
                                                    result.metadata.get('error_message', "Failed to generate video"))
                    return
                    
                # Clean up user state
                del self.waiting_for_prompt[user_id]
                if user_id in self.user_data:
                    del self.user_data[user_id]
                    
                task_id = result.data.get('task_id')
                e_context['reply'] = (
                    f"Video generation started with task ID: {task_id}\n"
                    "This may take 10-18 minutes. Please wait..."
                )

        except Exception as e:
            logger.error(f"[Image2Video] Error handling context: {e}")
            e_context['reply'] = f"An error occurred: {str(e)}"
