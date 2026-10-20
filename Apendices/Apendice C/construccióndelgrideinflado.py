import cv2
import numpy as np

def build_occupancy_grid(mask_nav_u8: np.ndarray,
                         cell_size_px: int,
                         tau_occ: float = 0.25) -> np.ndarray:
    """
    mask_nav_u8: imagen binaria uint8 (0 libre, 255 obstáculo)
    return: grid binario uint8 (0 libre, 1 ocupado), tamaño (Ny, Nx)
    """
    assert mask_nav_u8.ndim == 2
    h, w = mask_nav_u8.shape

    mask01 = (mask_nav_u8 > 0).astype(np.uint8)

    pad_h = (-h) % cell_size_px
    pad_w = (-w) % cell_size_px
    mask01 = np.pad(mask01, ((0, pad_h), (0, pad_w)), mode="constant", constant_values=1)

    hp, wp = mask01.shape
    ny, nx = hp // cell_size_px, wp // cell_size_px

    blocks = mask01.reshape(ny, cell_size_px, nx, cell_size_px)
    p_occ = blocks.mean(axis=(1, 3))

    grid = (p_occ >= tau_occ).astype(np.uint8)
    return grid

def inflate_obstacles(grid01: np.ndarray, radius_cells: int) -> np.ndarray:
    assert grid01.ndim == 2
    if radius_cells <= 0:
        return grid01.copy()

    k = 2 * radius_cells + 1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    inflated = cv2.dilate(grid01, kernel, iterations=1)
    return inflated