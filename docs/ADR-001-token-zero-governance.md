# ADR-001: Token-Zero Governance

## Status

Accepted

## Context

Operational AI systems fail in a particularly expensive way when governance starts after live inference is already eligible. Once inference begins, a system may spend tokens, produce plans, suggest tool use, or begin shaping downstream execution. That is already too late for a deterministic control boundary.

## Decision

Safety Valve enforces governance before inference. The public skeleton returns a deterministic receipt before any probabilistic generation is allowed to begin.

## Rationale

- Enforcement happens before inference because execution eligibility is the primary safety boundary.
- Post-hoc moderation is too late for operational systems because it reacts after tokens and routing opportunities are already exposed.
- Deterministic policy must precede probabilistic generation because governance needs stable, inspectable, repeatable outcomes.

## Consequences

- The gate stays small and auditable.
- The system can fail closed without invoking a model.
- Reviewable receipts exist even when execution is denied.
