from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Optional

Cell = Tuple[int, int]

@dataclass(frozen=True)
class Route:
    cells: List[Cell]
    cost: float

class ASRPort(ABC):
    @abstractmethod
    def listen_command(self) -> str:
        raise NotImplementedError

class TTSPort(ABC):
    @abstractmethod
    def speak(self, text: str) -> None:
        raise NotImplementedError

class RendererPort(ABC):
    @abstractmethod
    def render_overlay(self, route: Route, out_path: str) -> None:
        raise NotImplementedError

class NavigateUseCase:
    def __init__(self, asr: ASRPort, tts: TTSPort, renderer: RendererPort):
        self.asr = asr
        self.tts = tts
        self.renderer = renderer

    def run(self):
        cmd = self.asr.listen_command()
        self.tts.speak(f"Comando recibido: {cmd}")