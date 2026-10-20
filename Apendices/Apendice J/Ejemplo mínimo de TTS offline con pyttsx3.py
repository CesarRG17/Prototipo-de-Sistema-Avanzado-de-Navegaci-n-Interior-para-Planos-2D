import pyttsx3
from typing import Iterable

def speak_instructions(instructions: Iterable[str], rate: int = 170, volume: float = 1.0):
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)
    for msg in instructions:
        engine.say(msg)
    engine.runAndWait()