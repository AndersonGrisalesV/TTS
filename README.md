# 🗣️ Text-To-Speech App with Microsoft Edge-TTS

This project is a **simple, interactive Text-To-Speech (TTS) web app** built using [Streamlit](https://streamlit.io) and [edge-tts](https://pypi.org/project/edge-tts/). It allows you to **convert text into speech** using Microsoft's cloud TTS voices—directly in your browser.

## 🔑 Features

- ✅ Interactive web UI with [Streamlit](https://streamlit.io/)
- 🌐 Language selection using a locale map (`locales.json`)
- 🎙️ Dynamic voice selection (gender, locale, personality, etc.)
- 🎧 Audio playback and download (.mp3)
- 🔄 Voice list fetch/update from Microsoft's TTS service

## 📦 Dependencies

- Python 3.11+
- `streamlit >=1.45.1,<2.0.0`
- `edge-tts >=7.0.2,<8.0.0`

All managed via [Poetry](https://python-poetry.org/).

## 🚀 Setup & Usage

> You need [Poetry](https://python-poetry.org/docs/#installation) installed beforehand.

### 1. Clone the repo

```bash
git clone https://github.com/AndersonGrisalesV/TTS.git
cd tts
```

## 2. Install Poetry (if not already installed)

```bash
curl -sSL https://install.python-poetry.org | python -
```

## 3. Install dependencies using Poetry

```bash
poetry install
```

## 4. Activate the virtual environment

```bash
source .venv/Scripts/activate
```

or

```bash
source .venv/bin/activate
```

## 5. Run the TTS Project

```bash
streamlit run app.py
```
