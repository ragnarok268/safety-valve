        from __future__ import annotations

        from typing import List

        from ..pipeline import SafetyEvent


        def check_prompt(prompt: str) -> List[SafetyEvent]:
            """Toy no-op filter for the 'hallucination' category.

            In the real engine, this would contain tuned deterministic rules.
            Here it always returns an empty list.
            """
            return []
        