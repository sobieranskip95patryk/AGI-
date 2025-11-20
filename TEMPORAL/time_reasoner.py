# TEMPORAL/time_reasoner.py
"""
TimeReasoner: łączy EventManager i LTLEngine, ułatwia sprawdzanie właściwości temporalnych.
"""

from typing import List, Dict, Any
from .ltl_engine import LTLEngine
from .event_manager import EventManager, Event

class TimeReasoner:
    def __init__(self, event_manager: EventManager, ltl_engine: LTLEngine = None):
        self.event_manager = event_manager
        self.ltl = ltl_engine or LTLEngine()

    def trace_as_state_dicts(self):
        """
        Zamienia historię Eventów na sekwencję 'state' dictów,
        gdzie każde state zawiera atomy (event names) ustawione True w chwili ich wystąpienia.
        Można rozszerzyć: utrzymywać pamięć wartości, agregacje, sliding-window.
        """
        history = self.event_manager.get_history()
        states: List[Dict[str, Any]] = []
        for ev in history:
            states.append({ev.name: True, **ev.payload})
        return states

    def check_ltl(self, formula: str) -> bool:
        trace = self.trace_as_state_dicts()
        return self.ltl.evaluate_on_trace(formula, trace)