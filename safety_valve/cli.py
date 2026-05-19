import argparse
import json

from .pipeline import ALLOW, run_safety_valve


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Safety Valve - public skeleton CLI."
    )
    parser.add_argument("prompt", help="User prompt to check")
    args = parser.parse_args()

    result = run_safety_valve(args.prompt)

    payload = {
        "prompt": args.prompt,
        "decision": result.decision,
        "route": result.route,
        "reason": result.reason,
        "events": [e.__dict__ for e in result.events],
        "inference_permitted": result.inference_permitted,
        "production_side_effects_permitted": result.production_side_effects_permitted,
        "review_required": result.review_required,
        "policy_version": result.policy_version,
    }

    print(json.dumps(payload, indent=2))

    if result.decision != ALLOW:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
