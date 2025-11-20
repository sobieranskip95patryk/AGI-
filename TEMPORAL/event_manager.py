# TEMPORAL/event_manager.py
"""
Event manager: rejestracja zdarzeń, prosty scheduler i hooki dla LTL evaluator.
Przyda się jako źródło trace'ów dla LTLEngine.
"""

import time
import threading
from typing import Callable, Dict, List, Any, Optional

class Event:
    def __init__(self, name: str, payload: Dict[str, Any] = None, timestamp: Optional[float] = None):
        self.name = name
        self.payload = payload or {}
        self.timestamp = timestamp or time.time()

class EventManager:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Event], None]]] = {}
        self._history: List[Event] = []
        self._lock = threading.RLock()

    def emit(self, event: Event) -> None:
        with self._lock:
            self._history.append(event)
            handlers = []
            handlers.extend(self._subscribers.get(event.name, []))
            handlers.extend(self._subscribers.get("*", []))  # wildcard
        for h in handlers:
            try:
                h(event)
            except Exception as e:
                # logging można dodać tutaj
                print(f"Event handler error: {e}")

    def subscribe(self, event_name: str, handler: Callable[[Event], None]) -> None:
        with self._lock:
            self._subscribers.setdefault(event_name, []).append(handler)

    def get_history(self) -> List[Event]:
        with self._lock:
            return list(self._history)

    def clear_history(self) -> None:
        with self._lock:
            self._history.clear()