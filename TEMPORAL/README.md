TEMPORAL Module — LTL + Event Manager + Time Reasoner
----------------------------------------------------
Purpose:
- Evaluate simple LTL properties on finite traces.
- Provide event sourcing (EventManager) as trace provider.
- Provide TimeReasoner as integration surface for Planner/LogicEngine.

How to extend:
- Replace parse/evaluate with full LTL library (spot, tl, ltl3tools)
- Add sliding-window, stateful atoms, predicate evaluators
- Integrate with HTNPlanner to assert temporal constraints