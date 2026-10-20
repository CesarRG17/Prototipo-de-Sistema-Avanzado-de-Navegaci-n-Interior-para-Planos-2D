import json
import wave
from vosk import Model, KaldiRecognizer

def transcribe_vosk_wav(path_wav: str, model_dir: str, sample_rate: int = 16000) -> str:
    model = Model(model_dir)
    rec = KaldiRecognizer(model, sample_rate)

    with wave.open(path_wav, "rb") as wf:
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            rec.AcceptWaveform(data)

    out = json.loads(rec.FinalResult())
    return out.get("text", "")