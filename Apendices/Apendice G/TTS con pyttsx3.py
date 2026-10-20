  caption={TTS offline con pyttsx3 para instrucciones
  turn-by-turn
  (véase Sección~\ref{subsec:tts_pyttsx3}).},
  label={lst:anexo_pyttsx3_example}]
import pyttsx3
from typing import Iterable
 
def speak_instructions(instructions: Iterable[str],
                       rate: int = 170,
                       volume: float = 1.0) -> None:
    engine = pyttsx3.init()
    engine.setProperty("rate",   rate)
    engine.setProperty("volume", volume)
    for msg in instructions:
        engine.say(msg)
    engine.runAndWait()