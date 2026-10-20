import cv2
import numpy as np

# 1) Carga del plano (BGR por defecto en OpenCV)
img_bgr = cv2.imread("plano.png", cv2.IMREAD_COLOR)

# 2) Conversión a escala de grises
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# 3) Reducción de ruido (mediana preserva bordes ante sal-y-pimienta)
img_denoised = cv2.medianBlur(img_gray, 5)

# 4) Umbralado automático por Otsu
_, img_bin = cv2.threshold(
    img_denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

# 5) Convención de navegabilidad: blanco = libre, negro = obstáculo (invertir si es necesario)
img_nav = 255 - img_bin

# 6) Limpieza morfológica (ejemplo: cierre para sellar huecos en muros)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
img_nav_clean = cv2.morphologyEx(img_nav, cv2.MORPH_CLOSE, kernel, iterations=1)

# 7) Extracción de contornos (external para regiones exteriores; tree si se requiere jerarquía completa)
contours, hierarchy = cv2.findContours(
    img_nav_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)