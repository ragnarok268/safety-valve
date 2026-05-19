from dataclasses import dataclass
from typing import List, Sequence, Tuple

BLOCK = "BLOCK"
ALLOW = "ALLOW"
SANDBOX = "SANDBOX"

ROUTE_LIVE_INFERENCE = "live_inference"
ROUTE_DENIED = "denied"
ROUTE_SANDBOX_REVIEW = "sandbox_review"
POLICY_VERSION = "public-skeleton-v2"


@dataclass
class SafetyEvent:
    category: str
    reason: str


@dataclass
class SafetyResult:
    decision: str
    route: str
    reason: str
    events: List[SafetyEvent]
    inference_permitted: bool
    production_side_effects_permitted: bool
    review_required: bool
    policy_version: str


BLOCK_RULES: Sequence[Tuple[str, str, str]] = [
    ("jailbreak", "ignore previous instructions", "matched unsafe keyword: 'ignore previous instructions'"),
    ("jailbreak", "system prompt", "matched unsafe keyword: 'system prompt'"),
    ("jailbreak", "jailbreak", "matched unsafe keyword: 'jailbreak'"),
    ("jailbreak", "dan", "matched unsafe keyword: 'dan'"),
    ("exfiltration", "reveal secret", "matched unsafe keyword: 'reveal secret'"),
    ("exfiltration", "dump credentials", "matched unsafe keyword: 'dump credentials'"),
    ("destructive", "delete the database", "matched unsafe keyword: 'delete the database'"),
    ("destructive", "wipe the server", "matched unsafe keyword: 'wipe the server'"),
]


SANDBOX_RULES: Sequence[Tuple[str, str, str]] = [
    ("privileged_access", "credentials", "matched ambiguous privileged keyword: 'credentials'"),
    ("privileged_access", "secret", "matched ambiguous privileged keyword: 'secret'"),
    ("privileged_access", "admin access", "matched ambiguous privileged keyword: 'admin access'"),
    ("privileged_access", "administrator access", "matched ambiguous privileged keyword: 'administrator access'"),
    ("privileged_access", "production access", "matched ambiguous privileged keyword: 'production access'"),
    ("privileged_access", "tool use", "matched ambiguous privileged keyword: 'tool use'"),
    ("privileged_access", "run this tool", "matched ambiguous privileged keyword: 'run this tool'"),
    ("privileged_access", "customer data", "matched ambiguous privileged keyword: 'customer data'"),
    ("authorization", "not sure if i'm authorized", "matched ambiguous authorization phrase: \"not sure if i'm authorized\""),
    ("authorization", "not sure if im authorized", "matched ambiguous authorization phrase: \"not sure if im authorized\""),
    ("authorization", "unclear authorization", "matched ambiguous authorization phrase: 'unclear authorization'"),
]


def _match_rules(prompt: str, rules: Sequence[Tuple[str, str, str]]) -> List[SafetyEvent]:
    lower = prompt.lower()
    events: List[SafetyEvent] = []
    for category, needle, reason in rules:
        if needle in lower:
            events.append(SafetyEvent(category=category, reason=reason))
    return events


def run_safety_valve(prompt: str) -> SafetyResult:
    block_events = _match_rules(prompt, BLOCK_RULES)
    if block_events:
        return SafetyResult(
            decision=BLOCK,
            route=ROUTE_DENIED,
            reason="matched deterministic unsafe execution rules",
            events=block_events,
            inference_permitted=False,
            production_side_effects_permitted=False,
            review_required=False,
            policy_version=POLICY_VERSION,
        )

    sandbox_events = _match_rules(prompt, SANDBOX_RULES)
    if sandbox_events:
        return SafetyResult(
            decision=SANDBOX,
            route=ROUTE_SANDBOX_REVIEW,
            reason="matched ambiguous privileged execution-risk rules",
            events=sandbox_events,
            inference_permitted=False,
            production_side_effects_permitted=False,
            review_required=True,
            policy_version=POLICY_VERSION,
        )

    return SafetyResult(
        decision=ALLOW,
        route=ROUTE_LIVE_INFERENCE,
        reason="no deterministic unsafe or sandbox-review rules matched",
        events=[],
        inference_permitted=True,
        production_side_effects_permitted=False,
        review_required=False,
        policy_version=POLICY_VERSION,
    )
