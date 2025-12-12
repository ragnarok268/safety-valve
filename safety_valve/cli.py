import argparse
import json

from .pipeline import run_safety_valve, BLOCK


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Safety Valve – public skeleton CLI."
    )
    parser.add_argument("prompt", help="User prompt to check")
    args = parser.parse_args()

    result = run_safety_valve(args.prompt)

    payload = {
        "prompt": args.prompt,
        "decision": result.decision,
        "events": [e.__dict__ for e in result.events],
    }

    print(json.dumps(payload, indent=2))

    if result.decision == BLOCK:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

