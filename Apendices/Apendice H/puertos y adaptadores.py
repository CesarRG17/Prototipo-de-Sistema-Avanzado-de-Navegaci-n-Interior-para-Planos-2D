from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple
 
Cell = Tuple[int, int]
 
@dataclass(frozen=True)
class Route:
    cells: List[Cell]
    cost: float
 
# --- Puertos de salida (contratos que el dominio requiere) ---
 
class ASRPort(ABC):
    """Contrato para obtener un comando transcrito desde audio."""
    @abstractmethod
    def listen_command(self) -> str:
        raise NotImplementedError
 
class TTSPort(ABC):
    """Contrato para convertir texto a audio audible."""
    @abstractmethod
    def speak(self, text: str) -> None:
        raise NotImplementedError
 
class RendererPort(ABC):
    """Contrato para generar el overlay de ruta sobre el plano."""
    @abstractmethod
    def render_overlay(self, route: Route, out_path: str) -> None:
        raise NotImplementedError
 
# --- Caso de uso: orquestación extremo a extremo ---------------
 
class NavigateUseCase:
    """
    Coordina ASR, pathfinding, TTS y render sin depender de
    implementaciones concretas; recibe adaptadores por inyeccion
    de dependencias.
    """
    def __init__(self, asr: ASRPort, tts: TTSPort,
                 renderer: RendererPort) -> None:
        self.asr      = asr
        self.tts      = tts
        self.renderer = renderer
 
    def run(self) -> None:
        # 1. Captura el comando de voz del usuario
        cmd = self.asr.listen_command()
        # 2. Confirma el destino reconocido
        self.tts.speak(f"Navegando hacia: {cmd}")
        # 3. (pathfinding y render se invocan aqui con la ruta)