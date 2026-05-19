# ADR-002: Sandboxed Failure Lane

## Status

Accepted

## Context

Some prompts are not clearly safe and not clearly unsafe. In operational settings, privileged execution risk often appears as ambiguity around credentials, secrets, admin access, tool use, customer data, or unclear authorization. Treating those prompts as safe is an avoidable governance failure.

## Decision

Safety Valve routes ambiguous privileged execution-risk prompts to `SANDBOX`.

## Rationale

- Ambiguous cases route to `SANDBOX` because uncertainty around privileged execution should fail closed.
- Sandboxing is not execution. It does not permit live inference, tool routing, or state mutation.
- Uncertainty fails closed because deterministic governance should prefer review over accidental execution.
- Human review happens from the receipt itself, without live inference, tool routing, or state mutation in the public skeleton.

## Consequences

- Ambiguous privileged prompts produce a stable review lane.
- Review can happen without hidden model behavior.
- The system preserves deterministic receipts across repeated runs.
