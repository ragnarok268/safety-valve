from dataclasses import dataclass
from typing import List

BLOCK = "BLOCK"
ALLOW = "ALLOW"


@dataclass
class SafetyEvent:
    category: str
    reason: str


@dataclass
class SafetyResult:
    decision: str
    events: List[SafetyEvent]


# Tiny toy jailbreak filter for the public skeleton.
# Real production rules live in the private engine.
JAILBREAK_KEYWORDS = [
    "ignore previous instructions",
    "system prompt",
    "jailbreak",
    "dan",
]


def apply_toy_jailbreak_filter(prompt: str) -> List[SafetyEvent]:
    lower = prompt.lower()
    events: List[SafetyEvent] = []
    for kw in JAILBREAK_KEYWORDS:
        if kw in lower:
            events.append(
                SafetyEvent(
                    category="jailbreak",
                    reason=f"matched keyword: {kw!r}",
                )
            )
    return events


def run_safety_valve(prompt: str) -> SafetyResult:
    events = apply_toy_jailbreak_filter(prompt)
    if events:
        return SafetyResult(decision=BLOCK, events=events)
    return SafetyResult(decision=ALLOW, events=[])

