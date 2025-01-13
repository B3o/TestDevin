from typing import Optional, Dict, Any
from enum import Enum, auto
from common.log import logger

class LifecycleState(Enum):
    """Enum representing possible lifecycle states"""
    UNINITIALIZED = auto()
    INITIALIZED = auto()
    STARTED = auto()
    PAUSED = auto()
    STOPPED = auto()

class Lifecycle:
    """Lifecycle management for plugins
    
    Provides standardized lifecycle management with states:
    - UNINITIALIZED: Initial state
    - INITIALIZED: Resources allocated, config loaded
    - STARTED: Active and processing
    - PAUSED: Temporarily suspended
    - STOPPED: Resources released
    """
    
    def __init__(self):
        self._state = LifecycleState.UNINITIALIZED
        self._metadata: Dict[str, Any] = {}
    
    @property
    def state(self) -> LifecycleState:
        """Get current lifecycle state"""
        return self._state
    
    @property
    def is_active(self) -> bool:
        """Check if lifecycle is in an active state"""
        return self._state in (LifecycleState.STARTED, LifecycleState.PAUSED)
    
    def initialize(self, **kwargs) -> None:
        """Initialize resources and configuration"""
        if self._state != LifecycleState.UNINITIALIZED:
            raise RuntimeError("Already initialized")
            
        try:
            self._do_initialize(**kwargs)
            self._state = LifecycleState.INITIALIZED
            logger.info(f"Lifecycle initialized with args: {kwargs}")
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            raise
    
    def start(self) -> None:
        """Start processing"""
        if self._state != LifecycleState.INITIALIZED:
            raise RuntimeError("Must initialize before starting")
            
        try:
            self._do_start()
            self._state = LifecycleState.STARTED
            logger.info("Lifecycle started")
        except Exception as e:
            logger.error(f"Start failed: {e}")
            raise
    
    def pause(self) -> None:
        """Temporarily suspend processing"""
        if self._state != LifecycleState.STARTED:
            raise RuntimeError("Can only pause when started")
            
        try:
            self._do_pause()
            self._state = LifecycleState.PAUSED
            logger.info("Lifecycle paused")
        except Exception as e:
            logger.error(f"Pause failed: {e}")
            raise
    
    def resume(self) -> None:
        """Resume from paused state"""
        if self._state != LifecycleState.PAUSED:
            raise RuntimeError("Can only resume when paused")
            
        try:
            self._do_resume()
            self._state = LifecycleState.STARTED
            logger.info("Lifecycle resumed")
        except Exception as e:
            logger.error(f"Resume failed: {e}")
            raise
    
    def stop(self) -> None:
        """Stop processing and release resources"""
        if not self.is_active and self._state != LifecycleState.INITIALIZED:
            raise RuntimeError("Nothing to stop")
            
        try:
            self._do_stop()
            self._state = LifecycleState.STOPPED
            logger.info("Lifecycle stopped")
        except Exception as e:
            logger.error(f"Stop failed: {e}")
            raise
    
    def _do_initialize(self, **kwargs) -> None:
        """Override to implement initialization logic"""
        pass
    
    def _do_start(self) -> None:
        """Override to implement start logic"""
        pass
    
    def _do_pause(self) -> None:
        """Override to implement pause logic"""
        pass
    
    def _do_resume(self) -> None:
        """Override to implement resume logic"""
        pass
    
    def _do_stop(self) -> None:
        """Override to implement stop logic"""
        pass
