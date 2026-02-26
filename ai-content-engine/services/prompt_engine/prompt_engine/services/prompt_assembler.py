"""Prompt assembler - combines system, user, and few-shot prompts."""

import json


class PromptAssembler:
    """Assembles final prompts from components."""

    def assemble(
        self,
        system_prompt: str,
        user_prompt: str,
        few_shot_examples: dict | None = None,
    ) -> dict:
        final_system = system_prompt
        final_user = user_prompt

        if few_shot_examples and "examples" in few_shot_examples:
            examples_text = self._format_few_shot(few_shot_examples["examples"])
            final_user = f"{examples_text}\n\n{user_prompt}"

        return {
            "system_prompt": final_system,
            "user_prompt": final_user,
        }

    def _format_few_shot(self, examples: list[dict]) -> str:
        parts: list[str] = ["Here are some examples:", ""]
        for i, example in enumerate(examples, 1):
            input_text = example.get("input", "")
            output_text = example.get("output", "")
            if isinstance(output_text, dict):
                output_text = json.dumps(output_text, indent=2)
            parts.append(f"Example {i}:")
            parts.append(f"Input: {input_text}")
            parts.append(f"Output: {output_text}")
            parts.append("")
        parts.append("Now process the following:")
        return "\n".join(parts)
