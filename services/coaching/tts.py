from io import BytesIO
from gtts import gTTS


class TextToSpeech:
    def speak(self, text, lang="en"):
        cleaned = (text or "").strip()

        if not cleaned:
            return None

        normalized_lang = (lang or "en").strip().lower()
        if normalized_lang in ("hindi", "hi", "hi-in"):
            tts_lang = "hi"
        else:
            tts_lang = "en"

        buffer = BytesIO()

        gTTS(text=cleaned, lang=tts_lang).write_to_fp(buffer)

        buffer.seek(0)

        return buffer.read()