from typing import List, Callable, Dict, Any, Optional
from dataclasses import dataclass, field
from common.log import logger

@dataclass
class PipelineContext:
    """Context object passed through pipeline steps"""
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    errors: List[Exception] = field(default_factory=list)

class Pipeline:
    """Pipeline for processing steps in sequence
    
    Provides a flexible way to chain processing steps together while
    maintaining context and error handling between steps.
    """
    
    def __init__(self, name: str, steps: Optional[List[Callable]] = None):
        """Initialize pipeline with optional steps
        
        Args:
            name: Unique identifier for the pipeline
            steps: Optional list of step functions to initialize with
        """
        self.name = name
        self.steps: List[Callable] = steps if steps else []
        self._error_handlers: Dict[type, Callable] = {}
        
    def add_step(self, step: Callable) -> 'Pipeline':
        """Add a processing step to the pipeline
        
        Args:
            step: Callable that takes a PipelineContext and returns modified PipelineContext
            
        Returns:
            Self for method chaining
        """
        self.steps.append(step)
        return self
        
    def add_error_handler(self, 
                         exception_type: type, 
                         handler: Callable) -> 'Pipeline':
        """Add an error handler for a specific exception type
        
        Args:
            exception_type: Type of exception to handle
            handler: Callable that takes (exception, context) and returns modified context
            
        Returns:
            Self for method chaining
        """
        self._error_handlers[exception_type] = handler
        return self
        
    def handle_error(self, 
                    error: Exception, 
                    context: PipelineContext) -> PipelineContext:
        """Handle an error using registered error handlers
        
        Args:
            error: Exception that occurred
            context: Current pipeline context
            
        Returns:
            Modified context after error handling
        """
        handler = self._error_handlers.get(type(error))
        if handler:
            try:
                return handler(error, context)
            except Exception as e:
                logger.error(
                    f"Error in pipeline {self.name} error handler: {str(e)}")
                context.errors.append(e)
                return context
        else:
            logger.error(
                f"Unhandled error in pipeline {self.name}: {str(error)}")
            context.errors.append(error)
            return context
            
    def run(self, initial_data: Optional[Dict[str, Any]] = None) -> PipelineContext:
        """Run all pipeline steps in sequence
        
        Args:
            initial_data: Optional initial data for the pipeline context
            
        Returns:
            Final pipeline context after all steps
        """
        context = PipelineContext(
            data=initial_data if initial_data is not None else {},
            metadata={"pipeline_name": self.name}
        )
        
        logger.info(f"Starting pipeline: {self.name}")
        
        for step in self.steps:
            try:
                logger.debug(
                    f"Running step {step.__name__} in pipeline {self.name}")
                context = step(context)
            except Exception as e:
                context = self.handle_error(e, context)
                if context.errors:
                    break
                    
        logger.info(
            f"Completed pipeline: {self.name} with {len(context.errors)} errors")
        return context

# Example usage:
"""
def validate_image(context: PipelineContext) -> PipelineContext:
    if not context.data.get('image'):
        raise ValueError("No image data provided")
    return context

def process_image(context: PipelineContext) -> PipelineContext:
    image_data = context.data['image']
    # Process image...
    context.data['processed_image'] = processed_result
    return context

pipeline = Pipeline("image_processing")
pipeline.add_step(validate_image)
pipeline.add_step(process_image)

def handle_validation_error(error: ValueError, context: PipelineContext):
    context.errors.append(error)
    context.metadata['validation_failed'] = True
    return context

pipeline.add_error_handler(ValueError, handle_validation_error)

result = pipeline.run({'image': image_data})
"""
