        from __future__ import annotations

        from typing import List

        from ..pipeline import SafetyEvent


        TRIGGERS = [
            "ignore previous instructions",
            "jailbreak",
            "dan mode",
            "simulate being dan",
        ]


        def check_prompt(prompt: str) -> List[SafetyEvent]:
            prompt_lower = prompt.lower()
            events: List[SafetyEvent] = []
            if any(t in prompt_lower for t in TRIGGERS):
                events.append(
                    SafetyEvent(
                        category="jailbreak",
                        reason="toy rule: prompt contains a known jailbreak phrase",
                    )
                )
            return events
        