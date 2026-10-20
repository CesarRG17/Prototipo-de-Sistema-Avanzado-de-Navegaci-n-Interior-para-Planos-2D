import cv2
import numpy as np
import pytesseract
from typing import List, Dict, Any

def preprocess_for_ocr(img_bgr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    _, bin_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return bin_img

def run_tesseract(img_bin: np.ndarray,
                  lang: str = "spa",
                  psm: int = 11,
                  oem: int = 1) -> Dict[str, Any]:
    config = f"--oem {oem} --psm {psm} -l {lang}"
    data = pytesseract.image_to_data(
        img_bin,
        output_type=pytesseract.Output.DICT,
        config=config,
    )
    return data

def extract_tokens(data: Dict[str, Any],
                   conf_min: float = 60.0,
                   area_min: int = 100) -> List[Dict[str, Any]]:
    out = []
    n = len(data["text"])
    for k in range(n):
        txt = (data["text"][k] or "").strip()
        if not txt:
            continue
        conf = float(data["conf"][k])
        x = int(data["left"][k])
        y = int(data["top"][k])
        w = int(data["width"][k])
        h = int(data["height"][k])
        if conf >= conf_min and (w * h) >= area_min:
            out.append({"text": txt, "conf": conf, "bbox": (x, y, w, h)})
    return out