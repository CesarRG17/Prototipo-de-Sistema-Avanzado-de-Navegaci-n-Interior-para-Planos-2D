import numpy as np
from typing import List
 
 
def iou_binary(pred: np.ndarray, gt: np.ndarray) -> float:
    """
    Calcula IoU entre dos mascaras binarias.
    pred, gt: arrays 2D de dtype arbitrario; se binariza con > 0.
    Retorna 1.0 si ambas mascaras son completamente vacias.
    """
    pred_b = (pred > 0).astype(np.uint8)
    gt_b   = (gt   > 0).astype(np.uint8)
    inter  = np.logical_and(pred_b == 1, gt_b == 1).sum()
    union  = np.logical_or( pred_b == 1, gt_b == 1).sum()
    return float(inter) / float(union) if union > 0 else 1.0
 
 
def wer(ref: List[str], hyp: List[str]) -> float:
    """
    Calcula WER mediante distancia de edicion sobre palabras.
    ref: secuencia de palabras de referencia (N palabras).
    hyp: hipotesis del sistema ASR (M palabras).
    Retorna 0.0 si ref esta vacia.
    """
    n, m = len(ref), len(hyp)
    dp   = np.zeros((n + 1, m + 1), dtype=int)
    dp[:, 0] = np.arange(n + 1)
    dp[0, :] = np.arange(m + 1)
 
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost     = 0 if ref[i - 1] == hyp[j - 1] else 1
            dp[i, j] = min(
                dp[i - 1, j]     + 1,   # eliminacion
                dp[i, j - 1]     + 1,   # insercion
                dp[i - 1, j - 1] + cost # sustitucion / acierto
            )
 
    return float(dp[n, m]) / n if n > 0 else 0.0