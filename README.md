
# 🤖 AI-Driven Google Meet Interview Bot

An intelligent, automated system that joins Google Meet sessions, conducts interviews using AI-powered voice interactions, and logs results in Google Sheets for streamlined candidate evaluation.

---

## 📌 Problem Statement

Traditional interviews during large-scale hiring are time-consuming and labor-intensive. This project solves that by automating the initial screening process using a virtual bot that:
- Joins Google Meet automatically
- Conducts dynamic, AI-based interviews
- Analyzes and logs candidate responses in real-time

---

## 🎯 Project Objectives

- Automate preliminary interviews using voice-based AI
- Dynamically adapt questions based on candidate responses
- Log structured results into Google Sheets for HR teams

---

## 🧠 AI Components

| Feature | Technology |
|--------|------------|
| 🔊 **Text-to-Speech (TTS)** | Gemini API – To vocalize interview questions |
| 🎤 **Speech-to-Text (STT)** | OpenAI Whisper – For accurate response transcription |
| 🧠 **NLP & Reasoning** | Gemini – For understanding, evaluating, and generating follow-ups |
| 🔁 **Dialogue Management** | Gemini Context – Maintains flow and context during interviews |

---

## 🛠️ Technologies Used

- **Python** – Core language for logic and integration
- **Selenium** – Automates Google Meet browser interaction
- **Gemini Model** – For TTS and dialogue context
- **OpenAI Whisper** – For high-accuracy STT
- **LLM (Gemini)** – To generate questions and evaluate responses
- **Google Sheets** – For result logging and reporting

---

## ⚙️ System Architecture

```
[Browser Automation (Selenium)]
          ↓
[Google Meet Bot Joins]
          ↓
[AI Components]
   - TTS (Gemini)
   - STT (Whisper)
   - NLP + Follow-up Gen (LLM)
          ↓
[Logs & Scores]
→ Google Sheets
```

---

## 📦 Installation & Setup

1. **Download the Repository**
```bash
Download the zip file and extract it.
Open cmd line and change directory to the extracted folder
```

5. Additional Setup 

VB-Cable - 
To route the bot’s voice output (TTS) back into the microphone input (for STT), install a virtual audio cable:
- Extract the zip file "VBCABLE_Driver_Pack45" provided for VB Cable
- Run the installer provided in it (x64 installer is available for x64 machines)

FFMPEG - 
To manipulate audio internally in openai-whisper package.
- Extract the zip file "ffmpeg-2025-06-17-git-ee1f79b0fa-full_build" provided for FFMPEG
- Add the route to the bin folder inside the extracted folder to the system path variable


2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Up API Keys**
- Configure `config.py` with:
  - Gemini API Key
  - Generate a meeting and add a google meet link in the config

---

## 🚀 How to Run

```bash
python sheets.py
```

The bot will:
- Launch a browser session
- Join the specified Google Meet link
- Start the interview
- Ask AI generated questions to the interviewee
- Log transcription and summary to Google Sheets

---

## 📊 Output & Integration

- 🟩 **Structured Summary** – All interview data is stored in **Google Sheets**
- 📈 Includes transcribed responses, question logs, and score

---

## 📁 Folder Structure

```
INTERVIEW_BOT/
│
├── audio_channel.py            # Audio channel management (input/output routing)
├── bot_voice.py                # Bot's text-to-speech logic
├── config.py                   # Configuration and API key management
├── llm.py                      # LLM-based logic for questions & reasoning
├── main.py                     # Entry point of the application
├── sheets.py                   # Fetch interview info from sheet and start
├── requirements.txt            # Python dependencies
├── speech_to_text.py           # Handles audio input and speech recognition
├── temp.wav                    # Temporary audio file for TTS/STT loop

```

---

## ✅ Future Enhancements

- Integrated UI Dashboard
- CV + JD-Based Interview Customization
- Automated Scheduling via Google Calendar
- Automated Summary Generation & Email Sharing

---

## 🧑‍💼 Project Team

This project was developed by a passionate team of AI and automation enthusiasts:

- **Tanay Soni** 

- **Manan Soni**

- **Akash Verma**

- **Poorvi Agrawal**

---

## 📄 License

Copyright (c) 2025 . All rights reserved.
This code is provided for reference only. No permission is granted to use, modify, distribute, or reproduce this code in any form.
