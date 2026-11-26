import json
import time
import streamlit as st
import streamlit.components.v1 as components


class VoicePipeline:
    def __init__(self, llm, tts):
        self.llm = llm
        self.tts = tts
        self.last_spoken_at = 0

    def _find_form_issue(self, exercise, metrics):
        if "issue" in metrics:
            return metrics["issue"]

        if exercise == "Squats":
            depth = metrics.get("depth_status", "")
            back_angle = metrics.get("back_angle", 180)

            if depth == "TOO HIGH":
                return "The user's squat is not deep enough — knees are not bending sufficiently."

            if isinstance(back_angle, (int, float)) and back_angle < 130:
                return "The user is leaning too far forward during the squat."

        elif exercise == "Push-ups":
            alignment = metrics.get("body_alignment", "")
            hip_status = metrics.get("hip_status", "")

            if alignment == "Poor Form":
                return "The user's body is not straight during the push-up."

            if hip_status == "SAGGING":
                return "The user's hips are sagging down during the push-up."

            if hip_status == "PIKED UP":
                return "The user's hips are too high — lower them to form a straight line."

        elif exercise == "Biceps Curls (Dumbbell)":
            swing = metrics.get("swing_status", "")
            shoulder = metrics.get("shoulder_status", "")

            if swing == "SWINGING":
                return "The user is swinging their torso during the curl — keep the body still."

            if shoulder == "ELBOW DRIFTING":
                return "The user's elbow is drifting away from their side during the curl."

        elif exercise == "Shoulder Press":
            back_arch = metrics.get("back_arch_status", "")
            extension = metrics.get("extension_status", "")

            if back_arch == "Excessive Arch":
                return "The user is arching their lower back excessively during the press."

            if back_arch == "Slight Arch":
                return "Slight back arch detected — encourage the user to brace their core."

        elif exercise == "Lunges":
            balance = metrics.get("balance_status", "")

            if balance == "OFF BALANCE":
                return "The user is losing balance during the lunge — feet should be hip-width apart."

        return None

    def process_event(self, event, exercise, metrics):
        issue = self._find_form_issue(exercise, metrics)

        now = time.time()

        is_major_issue = event in ["workout_started", "set_completed", "workout_completed"]

        if not is_major_issue:
            if not issue:
                return None

            if now - self.last_spoken_at < 5:
                return None

        text = self.llm.give_feedback(event, issue)
        voice = self.tts.speak(text)

        self.last_spoken_at = now

        return voice, text


def autoplay_audio(audio_bytes, fallback_text=""):
    if audio_bytes:
        st.markdown(
            """
            <style>
            [data-testid='stAudio'] {
                position: fixed !important;
                left: -9999px !important;
                width: 1px !important;
                height: 1px !important;
                opacity: 0 !important;
                pointer-events: none !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    elif fallback_text:
        safe_text = json.dumps(fallback_text)
        components.html(
            f"""
            <script>
            (function() {{
                const synth = window.parent ? window.parent.speechSynthesis : window.speechSynthesis;
                if (synth) {{
                    synth.cancel();
                    const utter = new SpeechSynthesisUtterance({safe_text});
                    utter.lang = "en-US";
                    utter.rate = 1.02;
                    synth.speak(utter);
                }}
            }})();
            </script>
            """,
            height=0,
        )

    st.session_state.audio_to_play = None
    st.session_state.speak_fallback = False