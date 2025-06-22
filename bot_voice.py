import base64
import wave
from io import BytesIO
from google import genai
from google.genai import types
import device_selection
import pyaudio
import config

# Replace this with your Gemini API key
client = genai.Client(api_key=config.GEMINI_FREE_API)

def speak_with_gemini(text, voice_name="pulcherrima"):
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=text,
        config={
            "response_modalities": ["AUDIO"],
            "speech_config": {
                "voice_config": {
                    "prebuilt_voice_config": {"voice_name": voice_name}
                }
            }
        }
    )

#    print("text:", text)       # For testing purpose only

    # Handle failure case
    if not response.candidates or not response.candidates[0].content:
        print("❌ No TTS content returned from Gemini.")
        return

    try:
        raw_audio_base64 = response.candidates[0].content.parts[0].inline_data.data
    except Exception as e:
        print("❌ Failed to extract audio from Gemini response:", e)
        return

    raw_audio = base64.b64decode(raw_audio_base64)

    # Wrap raw PCM into WAV format
    buffer = BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(raw_audio)

    buffer.seek(0)
    wf = wave.open(buffer, 'rb')

    # Play audio
    p = pyaudio.PyAudio()
    device_index_tts = device_selection.device_index_tts() #4  # Or make this dynamic

    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
        output_device_index=device_index_tts
    )

    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("✅ Spoke via Gemini:", text)


# if __name__ == "__main__":
#    speak_with_gemini("My name is Tanay Soni, and I like to play guitar")