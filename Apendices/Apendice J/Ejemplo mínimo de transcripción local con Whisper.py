import whisper

def transcribe_whisper(path_audio: str, model_name: str = "base") -> str:
    model = whisper.load_model(model_name)
    out = model.transcribe(path_audio, language="es")
    return out.get("text", "").strip()