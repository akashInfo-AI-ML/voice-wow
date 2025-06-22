import pyaudio
import whisper
from io import BytesIO
import wave
import time
import audioop
import device_selection


DEVICE_INDEX_STT = device_selection.DEVICE_INDEX_STT() #1  # VB-Cable input
RATE = 16000                  # Sample rate (Hz). 24000 is good for speech.
CHUNK = 1024                  # Samples per frame
CHANNELS = 1                  # Mono audio
FORMAT = pyaudio.paInt16      # 16-bit audio format
SAMPLE_WIDTH = 2              # Bytes per sample for paInt16

# --- Silence Detection Configuration ---
SILENCE_THRESHOLD = 500       # RMS value below which audio is considered silent. Adjust this!
SILENCE_LIMIT_SECONDS = 2   # Seconds of continuous silence to stop recording.
INITIAL_TIMEOUT_SECONDS = 10

def record_audio_to_buffer():
    print("🎙️  Listening... (Waiting for sound)")

    audio = pyaudio.PyAudio()
    stream = None

    try:
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )

        frames = []
        audio_started = False
        silent_chunks = 0
        start_time = time.time()
        
        # Calculate how many silent chunks constitute the silence limit
        num_silent_chunks_to_stop = int(SILENCE_LIMIT_SECONDS * RATE / CHUNK)

        while True:
            data = stream.read(CHUNK)
            rms = audioop.rms(data, SAMPLE_WIDTH)  # Calculate RMS

            # --- Initial Timeout Logic ---
            if not audio_started and (time.time() - start_time) > INITIAL_TIMEOUT_SECONDS:
                print("No sound detected within the first 5 seconds. Stopping.")
                return None

            if rms > SILENCE_THRESHOLD:
                # Sound detected
                if not audio_started:
                    print("Speaking detected, recording has started...")
                    audio_started = True
                silent_chunks = 0
                frames.append(data)
            else:
                # Silence detected
                if audio_started:
                    silent_chunks += 1
                    frames.append(data) # Include trailing silence for natural sound
                    if silent_chunks > num_silent_chunks_to_stop:
                        print(f"Silence of {SILENCE_LIMIT_SECONDS} seconds detected. Stopping recording.")
                        break
    finally:
        # Cleanup
        if stream:
            stream.stop_stream()
            stream.close()
        if audio:
            audio.terminate()

    if not frames:
        print("No frames were recorded.")
        return None

    print("✅ Recording finished. Converting to WAV format...")

    # Convert the recorded frames to an in-memory WAV file
    buffer = BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(SAMPLE_WIDTH)
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

    return buffer


def transcribe_with_whisper():
    buffer = record_audio_to_buffer()
    
    if buffer is None:
        return "[ERROR: No audio recorded]"

    buffer.seek(0)  # ✅ This is crucial
    with open("temp.wav", "wb") as f:
        f.write(buffer.read())

    model = whisper.load_model("base")
    result = model.transcribe("temp.wav")
    print("📝 Transcription:", result['text'])
    return result['text']

