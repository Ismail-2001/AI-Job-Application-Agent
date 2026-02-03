from typing import Dict, Any, List, Callable
import logging

class EventBus:
    """
    A simple in-memory event bus to decouple application components.
    Allows for an extensible, event-driven architecture.
    """
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
        self.logger = logging.getLogger(__name__)

    def subscribe(self, event_type: str, listener: Callable):
        """Register a listener for a specific event type."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)
        self.logger.info(f"Subscribed {listener.__name__} to {event_type}")

    def emit(self, event_type: str, data: Any):
        """Emit an event and trigger all registered listeners."""
        self.logger.info(f"Emitting event: {event_type}")
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                try:
                    # In a real production system, this could be async/queued
                    listener(data)
                except Exception as e:
                    self.logger.error(f"Error in listener {listener.__name__} for {event_type}: {e}")

# Global instance
bus = EventBus()
