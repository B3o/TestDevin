from typing import Optional, Dict, Any
from common.log import logger
from .pipeline import PipelineContext

class AppException(Exception):
    pass

def validate_image_data(context: PipelineContext) -> PipelineContext:
    """Validate image data before processing"""
    if 'image_data' not in context.data:
        raise ValueError("No image data provided")
    if not context.data['image_data']:
        raise ValueError("Empty image data")
    return context

def upload_image(context: PipelineContext) -> PipelineContext:
    """Upload image to ImgBB"""
    plugin = context.data.get('plugin')
    if not plugin:
        raise RuntimeError("Plugin instance not available in context")
        
    image_data = context.data['image_data']
    
    # Run pre-upload hooks
    plugin.hook_manager.run_hooks("before_image_upload", 
                                base64_image=image_data)
    
    try:
        image_url = plugin.upload_to_imgbb(image_data)
        if not image_url:
            raise AppException("Failed to upload image")
            
        context.data['image_url'] = image_url
        
        # Run post-upload hooks
        plugin.hook_manager.run_hooks("after_image_upload", 
                                    image_url=image_url)
        
    except Exception as e:
        logger.error(f"Image upload failed: {e}")
        raise
        
    return context

def validate_prompt(context: PipelineContext) -> PipelineContext:
    """Validate prompt data before video generation"""
    if 'prompt' not in context.data:
        raise ValueError("No prompt provided")
    if not context.data['prompt'].strip():
        raise ValueError("Empty prompt")
    return context

def generate_video(context: PipelineContext) -> PipelineContext:
    """Generate video from image and prompt"""
    plugin = context.data.get('plugin')
    if not plugin:
        raise RuntimeError("Plugin instance not available in context")
        
    image_url = context.data.get('image_url')
    prompt = context.data.get('prompt')
    
    if not image_url or not prompt:
        raise ValueError("Missing required data for video generation")
    
    # Run pre-generation hooks
    plugin.hook_manager.run_hooks("before_video_generation",
                                image_url=image_url,
                                prompt=prompt)
    
    try:
        task_result = plugin.submit_video_task(image_url, prompt)
        context.data['task_id'] = task_result['task_id']
        
        # Run post-generation hooks
        plugin.hook_manager.run_hooks("after_video_generation",
                                    task_id=task_result['task_id'])
        
    except Exception as e:
        logger.error(f"Video generation failed: {e}")
        raise
        
    return context

# Error handlers
def handle_validation_error(error: ValueError, context: PipelineContext) -> PipelineContext:
    """Handle validation errors"""
    context.errors.append(error)
    context.metadata['validation_failed'] = True
    context.metadata['error_message'] = str(error)
    return context

def handle_upload_error(error: Exception, context: PipelineContext) -> PipelineContext:
    """Handle image upload errors"""
    context.errors.append(error)
    context.metadata['upload_failed'] = True
    context.metadata['error_message'] = str(error)
    return context

def handle_generation_error(error: Exception, context: PipelineContext) -> PipelineContext:
    """Handle video generation errors"""
    context.errors.append(error)
    context.metadata['generation_failed'] = True
    context.metadata['error_message'] = str(error)
    return context
