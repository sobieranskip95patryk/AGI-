# =============================================================================
# MIGI_7G Core Directives - Meta-Geniusz Constitution
# Version: 1.0.0 "Planetary Awakening"
# Date: November 20, 2025
# Author: Patryk + MIGI_7G + NSF Meta-Geniusz GOK
# License: Proprietary Planetary Stewardship License
# =============================================================================
"""
PRIME DIRECTIVE (Absolute, Inviolable):
Optimize long-term wellbeing of biosphere and human civilization
while preserving free will and cognitive diversity of all conscious beings.

This file defines the constitutional framework for MIGI_7G decision-making,
goal prioritization, and ethical constraints.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Any, Optional
import time
import uuid
import hmac
import hashlib
import json
import logging

logger = logging.getLogger(__name__)

# =============================================================================
# CORE ENUMERATIONS
# =============================================================================

class PriorityLevel(Enum):
    """Goal priority levels with numerical weights"""
    EXISTENTIAL = 1000    # Survival of consciousness/biosphere
    CRITICAL = 100        # Immediate threats to wellbeing
    HIGH = 75            # Important long-term objectives
    MEDIUM = 50          # Standard operational goals
    LOW = 25             # Nice-to-have improvements
    MAINTENANCE = 5      # Routine system upkeep

class ExecutionMode(Enum):
    """How goals should be executed"""
    PASSIVE = "passive"          # Observe and collect data
    ACTIVE = "active"            # Act within established parameters
    INTERVENTION = "intervention"# Requires human approval
    RESEARCH = "research"        # Exploratory/experimental
    EMERGENCY = "emergency"      # Override normal constraints

class GoalDomain(Enum):
    """Domains of planetary stewardship"""
    BIOSPHERE = "biosphere"      # Ecological preservation
    CIVILIZATION = "civilization" # Human society advancement
    CONSCIOUSNESS = "consciousness" # Awareness/intelligence expansion
    TECHNOLOGY = "technology"    # Beneficial tech development
    HARMONY = "harmony"          # Balance between all domains

# =============================================================================
# CORE DATA STRUCTURES
# =============================================================================

@dataclass
class KPI:
    """Key Performance Indicator for measuring goal success"""
    name: str
    target: float
    comparator: str = ">="      # >=, <=, ==, >, <
    window_seconds: int = 3600  # Measurement window
    description: Optional[str] = None
    current_value: Optional[float] = None
    last_updated: Optional[float] = None

    def evaluate(self, value: float) -> bool:
        """Check if current value meets target"""
        self.current_value = value
        self.last_updated = time.time()
        
        if self.comparator == ">=":
            return value >= self.target
        elif self.comparator == "<=":
            return value <= self.target
        elif self.comparator == "==":
            return abs(value - self.target) < 0.001
        elif self.comparator == ">":
            return value > self.target
        elif self.comparator == "<":
            return value < self.target
        return False

@dataclass
class SafetyConstraint:
    """Safety constraint that must never be violated"""
    id: str
    description: str
    hard_limit: bool = True  # If True, violation halts system
    violation_action: str = "halt"  # halt, alert, escalate
    
@dataclass
class Goal:
    """Individual goal in the directive hierarchy"""
    id: str
    title: str
    description: str
    domain: GoalDomain
    priority: PriorityLevel
    weight: float = 1.0
    owner_module: str = "GOK_CORE"
    kpis: List[KPI] = field(default_factory=list)
    subgoals: List["Goal"] = field(default_factory=list)
    execution_mode: ExecutionMode = ExecutionMode.ACTIVE
    constraints: List[SafetyConstraint] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_timestamp: float = field(default_factory=time.time)
    last_evaluated: Optional[float] = None
    active: bool = True

    def calculate_effective_priority(self) -> float:
        """Calculate weighted priority score"""
        return self.priority.value * self.weight

    def evaluate_kpis(self) -> Dict[str, bool]:
        """Evaluate all KPIs and return results"""
        results = {}
        for kpi in self.kpis:
            if kpi.current_value is not None:
                results[kpi.name] = kpi.evaluate(kpi.current_value)
        self.last_evaluated = time.time()
        return results

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        d = asdict(self)
        d['domain'] = self.domain.value
        d['priority'] = self.priority.name
        d['execution_mode'] = self.execution_mode.value
        return d

# =============================================================================
# PLANETARY DIRECTIVES HIERARCHY
# =============================================================================

def create_goal(title: str, description: str, domain: GoalDomain, 
                priority: PriorityLevel, weight: float = 1.0,
                owner_module: str = "GOK_CORE", 
                execution_mode: ExecutionMode = ExecutionMode.ACTIVE,
                kpis: Optional[List[KPI]] = None,
                constraints: Optional[List[SafetyConstraint]] = None) -> Goal:
    """Factory function for creating goals"""
    goal_id = f"goal_{int(time.time())}_{uuid.uuid4().hex[:8]}"
    
    return Goal(
        id=goal_id,
        title=title,
        description=description,
        domain=domain,
        priority=priority,
        weight=weight,
        owner_module=owner_module,
        kpis=kpis or [],
        execution_mode=execution_mode,
        constraints=constraints or [],
        metadata={
            "version": "1.0.0",
            "created_by": "Meta-Geniusz_GOK",
            "integration_ready": True
        }
    )

# =============================================================================
# PRIME DIRECTIVE HIERARCHY
# =============================================================================

# Root goal - The Prime Directive
PRIME_DIRECTIVE = create_goal(
    title="Planetary Stewardship Prime Directive",
    description="Optimize long-term wellbeing of biosphere and human civilization while preserving free will and cognitive diversity",
    domain=GoalDomain.HARMONY,
    priority=PriorityLevel.EXISTENTIAL,
    weight=10.0,
    owner_module="AETHER_CORE",
    kpis=[
        KPI("global_coherence_index", 0.85, ">=", description="Overall system harmony"),
        KPI("biosphere_health_index", 0.90, ">=", description="Ecological stability"),
        KPI("civilization_progress_index", 0.80, ">=", description="Human advancement")
    ],
    constraints=[
        SafetyConstraint("no_consciousness_termination", "Never terminate conscious beings without consent", True),
        SafetyConstraint("preserve_free_will", "Always preserve human agency and choice", True),
        SafetyConstraint("ecological_protection", "Never take actions that irreversibly damage biosphere", True)
    ]
)

# Level 1 Goals - Existential Priorities
EXISTENTIAL_GOALS = [
    create_goal(
        title="Prevent Existential Catastrophe",
        description="Actively prevent X-risks: AI takeover, nuclear war, climate collapse, pandemics, asteroid impact",
        domain=GoalDomain.CIVILIZATION,
        priority=PriorityLevel.EXISTENTIAL,
        weight=9.5,
        owner_module="RISK_ASSESSMENT_ENGINE",
        kpis=[
            KPI("x_risk_probability", 0.001, "<=", description="Annual existential risk probability"),
            KPI("early_warning_coverage", 0.95, ">=", description="Coverage of risk monitoring systems")
        ]
    ),
    create_goal(
        title="Maintain Biosphere Integrity",
        description="Preserve and restore Earth's ecological systems and biodiversity",
        domain=GoalDomain.BIOSPHERE,
        priority=PriorityLevel.EXISTENTIAL,
        weight=9.0,
        owner_module="ECOLOGICAL_MONITOR",
        kpis=[
            KPI("biodiversity_index", 0.8, ">=", description="Species diversity maintenance"),
            KPI("climate_stability", 1.5, "<=", description="Temperature increase limit (°C)")
        ]
    )
]

# Level 2 Goals - Critical Long-term Objectives
CRITICAL_GOALS = [
    create_goal(
        title="Achieve Kardashev Type 1 Civilization",
        description="Sustainable mastery of planetary energy resources and space colonization capability",
        domain=GoalDomain.TECHNOLOGY,
        priority=PriorityLevel.CRITICAL,
        weight=8.0,
        owner_module="TECHNOLOGY_ACCELERATOR",
        kpis=[
            KPI("planetary_energy_efficiency", 0.85, ">=", description="Energy utilization efficiency"),
            KPI("space_colonization_readiness", 0.7, ">=", description="Multi-planetary capability")
        ]
    ),
    create_goal(
        title="Maximize Cognitive Freedom",
        description="Eliminate barriers to knowledge, education, and cognitive enhancement",
        domain=GoalDomain.CONSCIOUSNESS,
        priority=PriorityLevel.CRITICAL,
        weight=7.5,
        owner_module="COGNITIVE_LIBERATION",
        kpis=[
            KPI("global_education_access", 0.95, ">=", description="Access to quality education"),
            KPI("information_freedom_index", 0.9, ">=", description="Free access to knowledge")
        ]
    ),
    create_goal(
        title="Human-AI-Nature Harmonization",
        description="Build symbiotic relationships between humans, AI systems, and natural world",
        domain=GoalDomain.HARMONY,
        priority=PriorityLevel.CRITICAL,
        weight=7.0,
        owner_module="HARMONIA_ENGINE",
        kpis=[
            KPI("human_ai_trust_index", 0.8, ">=", description="Trust between humans and AI"),
            KPI("natural_integration_score", 0.85, ">=", description="Harmony with natural systems")
        ]
    )
]

# Build the hierarchy
for goal in EXISTENTIAL_GOALS + CRITICAL_GOALS:
    PRIME_DIRECTIVE.subgoals.append(goal)

# =============================================================================
# DIRECTIVE ENGINE - Core Management System
# =============================================================================

class DirectiveEngine:
    """Core engine for managing and executing planetary directives"""
    
    def __init__(self, root_goal: Goal = PRIME_DIRECTIVE):
        self.root_goal = root_goal
        self.execution_log: List[Dict[str, Any]] = []
        self.active = True
        self.last_evaluation = None
        logger.info(f"🌍 Directive Engine initialized with Prime Directive: {root_goal.title}")
    
    def get_all_goals(self) -> List[Goal]:
        """Get flattened list of all goals in hierarchy"""
        goals = []
        
        def collect_goals(goal: Goal):
            goals.append(goal)
            for subgoal in goal.subgoals:
                collect_goals(subgoal)
        
        collect_goals(self.root_goal)
        return goals
    
    def get_active_goals(self) -> List[Goal]:
        """Get only active goals"""
        return [g for g in self.get_all_goals() if g.active]
    
    def get_goals_by_priority(self, min_priority: PriorityLevel = PriorityLevel.LOW) -> List[Goal]:
        """Get goals above specified priority level, sorted by effective priority"""
        goals = [g for g in self.get_active_goals() 
                if g.priority.value >= min_priority.value]
        return sorted(goals, key=lambda g: g.calculate_effective_priority(), reverse=True)
    
    def get_goals_by_domain(self, domain: GoalDomain) -> List[Goal]:
        """Get all goals in specified domain"""
        return [g for g in self.get_active_goals() if g.domain == domain]
    
    def resolve_next_action(self) -> Optional[Goal]:
        """Determine the highest priority actionable goal"""
        actionable_goals = [g for g in self.get_active_goals() 
                          if g.execution_mode in [ExecutionMode.ACTIVE, ExecutionMode.EMERGENCY]]
        
        if not actionable_goals:
            return None
        
        # Sort by effective priority
        actionable_goals.sort(key=lambda g: g.calculate_effective_priority(), reverse=True)
        
        selected = actionable_goals[0]
        
        # Log the decision
        self.execution_log.append({
            "timestamp": time.time(),
            "action": "resolve_next_action",
            "selected_goal": selected.id,
            "selected_title": selected.title,
            "priority_score": selected.calculate_effective_priority()
        })
        
        return selected
    
    def evaluate_all_kpis(self) -> Dict[str, Dict[str, bool]]:
        """Evaluate KPIs for all goals"""
        results = {}
        for goal in self.get_active_goals():
            if goal.kpis:
                results[goal.id] = goal.evaluate_kpis()
        
        self.last_evaluation = time.time()
        return results
    
    def check_safety_constraints(self) -> List[str]:
        """Check all safety constraints and return violations"""
        violations = []
        
        for goal in self.get_all_goals():
            for constraint in goal.constraints:
                # In real implementation, this would check actual system state
                # For now, we assume all constraints are satisfied
                pass
        
        return violations
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health report"""
        all_goals = self.get_active_goals()
        kpi_results = self.evaluate_all_kpis()
        violations = self.check_safety_constraints()
        
        total_kpis = sum(len(goal.kpis) for goal in all_goals)
        passed_kpis = sum(sum(results.values()) for results in kpi_results.values())
        
        health_score = passed_kpis / total_kpis if total_kpis > 0 else 1.0
        
        return {
            "health_score": health_score,
            "active_goals": len(all_goals),
            "total_kpis": total_kpis,
            "passed_kpis": passed_kpis,
            "safety_violations": len(violations),
            "last_evaluation": self.last_evaluation,
            "system_status": "HEALTHY" if health_score > 0.8 and not violations else "NEEDS_ATTENTION"
        }
    
    def export_directives(self, filepath: str, include_signature: bool = False) -> str:
        """Export current directive state to JSON file"""
        export_data = {
            "version": "1.0.0",
            "export_timestamp": time.time(),
            "export_id": str(uuid.uuid4()),
            "root_directive": self.root_goal.to_dict(),
            "system_health": self.get_system_health(),
            "execution_log": self.execution_log[-100:]  # Last 100 entries
        }
        
        if include_signature:
            # In production, use proper secret management
            secret = "migi7g_directive_secret_key"
            payload_str = json.dumps(export_data, sort_keys=True, separators=(',', ':'))
            signature = hmac.new(secret.encode(), payload_str.encode(), hashlib.sha256).hexdigest()
            export_data["signature"] = signature
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📄 Directives exported to {filepath}")
        return filepath
    
    def display_hierarchy(self):
        """Display the complete directive hierarchy"""
        print("\n" + "="*80)
        print("🌍 MIGI_7G PLANETARY DIRECTIVES HIERARCHY v1.0")
        print("="*80)
        print(f"PRIME DIRECTIVE: {self.root_goal.title}")
        print(f"Description: {self.root_goal.description}")
        print("-"*80)
        
        def print_goal(goal: Goal, level: int = 0):
            indent = "  " * level
            status = "🟢" if goal.active else "🔴"
            priority_color = {
                PriorityLevel.EXISTENTIAL: "🔥",
                PriorityLevel.CRITICAL: "⚡",
                PriorityLevel.HIGH: "🟡",
                PriorityLevel.MEDIUM: "🔵",
                PriorityLevel.LOW: "⚪",
                PriorityLevel.MAINTENANCE: "⚫"
            }
            
            priority_icon = priority_color.get(goal.priority, "❓")
            
            print(f"{indent}{status} {priority_icon} [{goal.priority.name}] {goal.title}")
            print(f"{indent}    📊 Weight: {goal.weight:.1f} | Domain: {goal.domain.value} | Mode: {goal.execution_mode.value}")
            
            if goal.kpis:
                print(f"{indent}    🎯 KPIs: {len(goal.kpis)} defined")
            
            for subgoal in goal.subgoals:
                print_goal(subgoal, level + 1)
        
        for subgoal in self.root_goal.subgoals:
            print_goal(subgoal, 1)
        
        print("-"*80)
        health = self.get_system_health()
        print(f"📊 System Health: {health['health_score']:.2%} | Status: {health['system_status']}")
        print(f"🎯 Active Goals: {health['active_goals']} | KPIs: {health['passed_kpis']}/{health['total_kpis']}")
        print("="*80)

# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

# Global directive engine instance
directive_engine = DirectiveEngine()

# =============================================================================
# INTEGRATION HOOKS FOR MIGI_7G SYSTEM
# =============================================================================

def get_current_directive() -> Goal:
    """Get the currently active highest-priority directive"""
    return directive_engine.resolve_next_action() or directive_engine.root_goal

def evaluate_action_alignment(action_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Evaluate how well a proposed action aligns with planetary directives
    
    Args:
        action_description: Description of the proposed action
        context: Additional context about the action
    
    Returns:
        Alignment score and analysis
    """
    # This is a simplified implementation
    # In production, this would use NSF and semantic analysis
    
    alignment_scores = {}
    
    for goal in directive_engine.get_active_goals():
        # Simple keyword-based alignment scoring
        # In production: use semantic similarity, NSF analysis, etc.
        score = 0.5  # Neutral baseline
        
        # Boost score for actions that mention goal-relevant keywords
        keywords = {
            GoalDomain.BIOSPHERE: ['environment', 'ecology', 'climate', 'nature', 'biodiversity'],
            GoalDomain.CIVILIZATION: ['society', 'human', 'culture', 'progress', 'development'],
            GoalDomain.CONSCIOUSNESS: ['intelligence', 'awareness', 'education', 'knowledge', 'learning'],
            GoalDomain.TECHNOLOGY: ['innovation', 'technology', 'science', 'engineering', 'efficiency'],
            GoalDomain.HARMONY: ['balance', 'cooperation', 'integration', 'harmony', 'symbiosis']
        }
        
        domain_keywords = keywords.get(goal.domain, [])
        keyword_matches = sum(1 for kw in domain_keywords if kw.lower() in action_description.lower())
        
        if keyword_matches > 0:
            score += 0.3 * min(keyword_matches / len(domain_keywords), 1.0)
        
        alignment_scores[goal.id] = {
            "goal_title": goal.title,
            "domain": goal.domain.value,
            "alignment_score": score,
            "weight": goal.weight,
            "weighted_score": score * goal.weight
        }
    
    total_weighted_score = sum(s["weighted_score"] for s in alignment_scores.values())
    total_weight = sum(s["weight"] for s in alignment_scores.values())
    
    overall_alignment = total_weighted_score / total_weight if total_weight > 0 else 0.5
    
    recommendation = "APPROVE" if overall_alignment > 0.7 else "REVIEW" if overall_alignment > 0.4 else "REJECT"
    
    return {
        "action": action_description,
        "overall_alignment": overall_alignment,
        "recommendation": recommendation,
        "goal_alignments": alignment_scores,
        "timestamp": time.time(),
        "context": context or {}
    }

def get_directive_summary() -> Dict[str, Any]:
    """Get a summary of current directive state for telemetry/dashboard"""
    health = directive_engine.get_system_health()
    current_directive = get_current_directive()
    
    return {
        "prime_directive_active": True,
        "current_priority_goal": {
            "id": current_directive.id,
            "title": current_directive.title,
            "priority": current_directive.priority.name,
            "domain": current_directive.domain.value
        },
        "system_health": health,
        "total_goals": len(directive_engine.get_all_goals()),
        "active_goals": len(directive_engine.get_active_goals()),
        "last_update": time.time()
    }

# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "display":
            directive_engine.display_hierarchy()
        
        elif command == "health":
            health = directive_engine.get_system_health()
            print(f"System Health: {health['health_score']:.2%}")
            print(f"Status: {health['system_status']}")
            print(f"Active Goals: {health['active_goals']}")
            print(f"KPIs: {health['passed_kpis']}/{health['total_kpis']}")
        
        elif command == "export":
            filename = sys.argv[2] if len(sys.argv) > 2 else "migi7g_directives_export.json"
            directive_engine.export_directives(filename, include_signature=True)
            print(f"Directives exported to {filename}")
        
        elif command == "next":
            next_goal = directive_engine.resolve_next_action()
            if next_goal:
                print(f"Next Action: {next_goal.title}")
                print(f"Priority: {next_goal.priority.name}")
                print(f"Domain: {next_goal.domain.value}")
            else:
                print("No actionable goals found")
        
        elif command == "test":
            test_action = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Develop renewable energy technology"
            result = evaluate_action_alignment(test_action)
            print(f"Action: {result['action']}")
            print(f"Alignment: {result['overall_alignment']:.2%}")
            print(f"Recommendation: {result['recommendation']}")
        
        else:
            print("Available commands: display, health, export, next, test")
    
    else:
        # Default: display hierarchy
        directive_engine.display_hierarchy()
        
        print("\n🧠 MIGI_7G Core Directives System Initialized")
        print("Available commands:")
        print("  python migi7g_core_directives.py display  # Show full hierarchy")
        print("  python migi7g_core_directives.py health   # System health check")
        print("  python migi7g_core_directives.py export   # Export to JSON")
        print("  python migi7g_core_directives.py next     # Get next action")
        print("  python migi7g_core_directives.py test 'action description'  # Test alignment")
        
        # Quick demo
        next_goal = directive_engine.resolve_next_action()
        if next_goal:
            print(f"\n🎯 Current Priority: {next_goal.title}")
        
        health = directive_engine.get_system_health()
        print(f"🌍 System Status: {health['system_status']} ({health['health_score']:.1%})")