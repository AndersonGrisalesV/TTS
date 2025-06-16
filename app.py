import streamlit as st
import asyncio
import os
import json
from tts_util import tts, fetch_voices  # Ensure fetch_voices is implemented

# --- Constants ---
AUDIO_FOLDER = "generated_audio"
VOICE_FILE = "voices.json"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# --- Load locale-language map ---
LOCALE_FILE = "locales.json"
if os.path.exists(LOCALE_FILE):
    with open(LOCALE_FILE, "r", encoding="utf-8") as f:
        LOCALE_LANGUAGE_MAP = json.load(f)
else:
    st.error("❌ Missing 'locales.json'. Please make sure it exists.")
    LOCALE_LANGUAGE_MAP = {}


# --- Streamlit setup ---
st.set_page_config(page_title="Text to Speech App", layout="centered")
st.title("🗣️ Text to Speech with Edge-TTS")

# --- Update voice list ---
if st.button("🔄 Update Voice List"):
    st.info("Updating available voices...")
    voices = asyncio.run(fetch_voices())
    with open(VOICE_FILE, "w", encoding="utf-8") as f:
        json.dump(voices, f, indent=2)
    st.success("Voice list updated!")

# --- Load voices ---
if os.path.exists(VOICE_FILE):
    with open(VOICE_FILE, "r", encoding="utf-8") as f:
        voice_list = json.load(f)

    # Extract available language codes
    available_lang_codes = sorted(
        set(v["Locale"].split("-")[0] for v in voice_list))
    lang_code_to_name = {code: LOCALE_LANGUAGE_MAP.get(
        code, code) for code in available_lang_codes}
    name_to_lang_code = {v: k for k, v in lang_code_to_name.items()}
    available_lang_names = sorted(name_to_lang_code.keys())

    # --- UI: language select ---
    default_language_name = "🇺🇸 English"
    selected_language_name = st.selectbox(
        "🌐 Choose a language:",
        available_lang_names,
        index=available_lang_names.index(default_language_name)
        if default_language_name in available_lang_names else 0
    )
    selected_lang_code = name_to_lang_code[selected_language_name]

    # --- Filter voices by language ---
    def format_voice(v):
        friendly = v.get("FriendlyName", "").replace(
            "Microsoft ", "").replace("Online (Natural)", "").strip()
        gender = v.get("Gender", "")
        locale = v.get("Locale", "")
        short = v.get("ShortName", "")
        personalities = ", ".join(
            v.get("VoiceTag", {}).get("VoicePersonalities", []))
        return f"{friendly} - {locale} [{gender}] - {personalities} ({short})"

    filtered_voices = [v for v in voice_list if v.get(
        "Locale", "").startswith(selected_lang_code)]
    voice_display_map = {format_voice(
        v): v["ShortName"] for v in filtered_voices}
    voice_display_names = list(voice_display_map.keys())

    # --- Default to BrianMultilingual if available ---
    default_voice_key = next(
        (name for name in voice_display_names if "en-US-BrianMultilingualNeural" in name),
        voice_display_names[0] if voice_display_names else ""
    )

    if voice_display_names:
        selected_display_name = st.selectbox(
            "🎙️ Choose a voice:",
            voice_display_names,
            index=voice_display_names.index(default_voice_key)
        )
        voice = voice_display_map[selected_display_name]
    else:
        st.warning("⚠️ No voices available for this language.")
        voice = None
else:
    st.error("❌ Voice list not found. Please click '🔄 Update Voice List'.")
    voice = None

# --- Input and generation ---
text_input = st.text_area(
    "Enter the text you want to convert to speech:", height=200)
generate_btn = st.button("🎤 Generate Speech")

if generate_btn and text_input.strip() and voice:
    existing_files = [f for f in os.listdir(
        AUDIO_FOLDER) if f.startswith("ai_audio") and f.endswith(".mp3")]
    numbers = [int(f.split("ai_audio")[1].split(".mp3")[0])
               for f in existing_files if f.split("ai_audio")[1].split(".mp3")[0].isdigit()]
    next_num = max(numbers + [0]) + 1
    audio_file = os.path.join(AUDIO_FOLDER, f"ai_audio{next_num}.mp3")

    with st.spinner("Generating speech..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            tts(text_input, voice=voice, outfile=audio_file))

    st.success(f"✅ Speech generated as ai_audio{next_num}.mp3!")

    with open(audio_file, "rb") as file:
        audio_bytes = file.read()
        st.audio(audio_bytes, format="audio/mp3")
        st.download_button(
            label="📥 Download Audio",
            data=audio_bytes,
            file_name=f"ai_audio{next_num}.mp3",
            mime="audio/mpeg"
        )
