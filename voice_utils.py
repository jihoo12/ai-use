"""AI 면접 코치용 음성 공통 함수.
수업의 STT(귀) → LLM(머리) → TTS(입) 구조를 그대로 사용합니다.
"""
import base64, json, re
from pathlib import Path
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

STT_MODEL = "gemini-3.5-transcribe"
LLM_MODEL = "gemini-3.8-flash"
TTS_MODEL = "gemini-3.8-flash-tts"

REC = Path("recordings")
REC.mkdir(exist_ok=True)

def record(filename, seconds=5, sr=16000, countdown=True):
    if countdown:
        import time
        for n in (3, 2, 1):
            print(f"{n}...", end=" ", flush=True)
            time.sleep(0.7)
    print(f"\n[녹음] {seconds}초 동안 말하세요 🎙")
    data = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype="int16")
    sd.wait()
    path = REC / filename
    sf.write(path, data, sr)
    print("[녹음] 완료:", path)
    return str(path)

def listen(path, autoplay=False):
    from IPython.display import Audio, display
    display(Audio(filename=str(path), autoplay=autoplay))

def stt(path, lang=None, smart=False):
    uploaded = client.files.upload(file=path)
    cfg = {}
    if lang:
        cfg["language_codes"] = [lang]
    if smart:
        cfg["mode"] = "smart"
    kwargs = {
        "model": STT_MODEL,
        "input": [{"type": "audio", "uri": uploaded.uri, "mime_type": uploaded.mime_type}],
    }
    if cfg:
        kwargs["generation_config"] = {"transcription_config": cfg}
    r = client.interactions.create(**kwargs)
    return (r.output_text or "").strip()

def llm(prompt):
    r = client.interactions.create(model=LLM_MODEL, input=prompt)
    return (r.output_text or "").strip()

def llm_json(prompt):
    raw = llm(prompt + "\nReturn ONLY valid JSON. No code fences, no explanations.")
    raw = re.sub(r"^```(json)?|```$", "", raw.strip(), flags=re.M).strip()
    m = re.search(r"\{.*\}", raw, flags=re.S)
    return json.loads(m.group(0) if m else raw)

def tts(text, voice="Kore", style=None, filename="tts.wav"):
    item = {"type": "text", "text": text}
    if style:
        item["annotations"] = [{"type": "speech_metadata", "style": style}]
    r = client.interactions.create(
        model=TTS_MODEL,
        input=[{"type": "user_input", "content": [item]}],
        response_format={"type": "audio"},
        generation_config={"speech_config": [{"voice": voice}]},
    )
    out = REC / filename
    out.write_bytes(base64.b64decode(r.output_audio.data))
    return str(out)

def usage():
    print("이 간소화 버전은 API 호출 횟수를 별도로 기록하지 않습니다.")
