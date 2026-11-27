from services.config.workout_config import PROMPT


class LLMCoach:
    def __init__(self, groq_client):
        self.client = groq_client
        self.history = []
        self.system_prompt = PROMPT

    def give_feedback(self, event, issue, language="English"):
        lang_mode = (language or "English").strip().lower()
        if lang_mode in ("hindi", "hi"):
            lang_instruction = (
                "Respond ONLY in natural, easy-to-understand Hindi "
                "(use Devanagari script with natural gym coaching terms, concise and encouraging)."
            )
        else:
            lang_instruction = "Respond ONLY in clear, concise English."

        prompt = f"Language: {lang_instruction}\nEvent: {event}"

        if issue:
            prompt += f"\nForm Issue: {issue}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.history[-10:],
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.4,
        )

        text = response.choices[0].message.content.strip()
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": text})

        return text