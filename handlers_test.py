import pytest
from unittest.mock import MagicMock, patch
from .pipeline import PipelineContext
from .handlers import (
    validate_image_data,
    upload_image,
    validate_prompt,
    generate_video,
    handle_validation_error
)

def test_validate_image_data():
    # Test valid case
    context = PipelineContext(data={'image_data': 'test_data'})
    result = validate_image_data(context)
    assert result.data['image_data'] == 'test_data'
    
    # Test missing image data
    context = PipelineContext(data={})
    with pytest.raises(ValueError):
        validate_image_data(context)
        
    # Test empty image data
    context = PipelineContext(data={'image_data': ''})
    with pytest.raises(ValueError):
        validate_image_data(context)

def test_upload_image():
    mock_plugin = MagicMock()
    mock_plugin.upload_to_imgbb.return_value = 'test_url'
    
    context = PipelineContext(data={
        'plugin': mock_plugin,
        'image_data': 'test_data'
    })
    
    result = upload_image(context)
    assert result.data['image_url'] == 'test_url'
    mock_plugin.hook_manager.run_hooks.assert_called()
    
    # Test upload failure
    mock_plugin.upload_to_imgbb.return_value = None
    with pytest.raises(Exception):
        upload_image(context)

def test_validate_prompt():
    # Test valid case
    context = PipelineContext(data={'prompt': 'test prompt'})
    result = validate_prompt(context)
    assert result.data['prompt'] == 'test prompt'
    
    # Test missing prompt
    context = PipelineContext(data={})
    with pytest.raises(ValueError):
        validate_prompt(context)
        
    # Test empty prompt
    context = PipelineContext(data={'prompt': '  '})
    with pytest.raises(ValueError):
        validate_prompt(context)

def test_generate_video():
    mock_plugin = MagicMock()
    mock_plugin.submit_video_task.return_value = {'task_id': 'test_task'}
    
    context = PipelineContext(data={
        'plugin': mock_plugin,
        'image_url': 'test_url',
        'prompt': 'test prompt'
    })
    
    result = generate_video(context)
    assert result.data['task_id'] == 'test_task'
    mock_plugin.hook_manager.run_hooks.assert_called()
    
    # Test missing data
    context = PipelineContext(data={'plugin': mock_plugin})
    with pytest.raises(ValueError):
        generate_video(context)

def test_error_handling():
    context = PipelineContext()
    error = ValueError("Test error")
    
    result = handle_validation_error(error, context)
    assert len(result.errors) == 1
    assert result.metadata['validation_failed']
    assert result.metadata['error_message'] == "Test error"
