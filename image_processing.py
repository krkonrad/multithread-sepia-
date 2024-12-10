import numpy as np
from PIL import Image
import multiprocessing as mp
import time

def apply_sepia(image_array):
    """
    Zastosuj filtr sepii do tablicy obrazu.

    Args:
        image_array (np.ndarray): Tablica NumPy reprezentująca obraz RGB.

    Returns:
        np.ndarray: Tablica NumPy z zastosowanym filtrem sepii.
    """
    # Macierz filtra sepii
    sepia_filter = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    # Mnożenie tablicy obrazu przez macierz filtra
    sepia_image = image_array @ sepia_filter.T
    # Ograniczenie wartości do zakresu 0-255
    sepia_image = np.clip(sepia_image, 0, 255)
    return sepia_image.astype(np.uint8)

def split_image(image_array, num_segments):
    """
    Podziel tablicę obrazu na segmenty wzdłuż osi pionowej.

    Args:
        image_array (np.ndarray): Tablica NumPy reprezentująca obraz RGB.
        num_segments (int): Liczba segmentów, na które podzielić obraz.

    Returns:
        list: Lista segmentów obrazu.
    """
    # Wyznacz wysokość każdego segmentu
    height = image_array.shape[0]
    segment_height = height // num_segments
    segments = []

    for i in range(num_segments):
        start = i * segment_height
        end = (i + 1) * segment_height if i < num_segments - 1 else height
        segments.append(image_array[start:end])

    return segments

def process_segment(segment):
    """
    Przetwórz segment obrazu, stosując filtr sepii.

    Args:
        segment (np.ndarray): Segment obrazu.

    Returns:
        np.ndarray: Przetworzony segment obrazu.
    """
    return apply_sepia(segment)

def merge_segments(segments):
    """
    Połącz listę segmentów obrazu w jedną tablicę obrazu.

    Args:
        segments (list): Lista segmentów obrazu.

    Returns:
        np.ndarray: Połączona tablica obrazu.
    """
    return np.vstack(segments)

def apply_sepia_parallel(image_path, save_path, num_workers=4):
    """
    Zastosuj filtr sepii do obrazu z użyciem przetwarzania równoległego.

    Args:
        image_path (str): Ścieżka do pliku wejściowego obrazu.
        save_path (str): Ścieżka do zapisu przetworzonego obrazu.
        num_workers (int): Liczba procesów roboczych.

    Returns:
        float: Czas przetwarzania w sekundach.
    """
    start_time = time.time()
    image = Image.open(image_path).convert('RGB')
    image_array = np.array(image)

    # Podział obrazu na segmenty
    segments = split_image(image_array, num_workers)

    # Przetwarzanie segmentów równolegle
    with mp.Pool(processes=num_workers) as pool:
        processed_segments = pool.map(process_segment, segments)

    # Połączenie segmentów w pełny obraz
    sepia_image_array = merge_segments(processed_segments)
    sepia_image = Image.fromarray(sepia_image_array)
    sepia_image.save(save_path)

    elapsed_time = time.time() - start_time
    return elapsed_time

def apply_sepia_single(image_path, save_path):
    """
    Zastosuj filtr sepii do obrazu bez użycia przetwarzania równoległego.

    Args:
        image_path (str): Ścieżka do pliku wejściowego obrazu.
        save_path (str): Ścieżka do zapisu przetworzonego obrazu.

    Returns:
        float: Czas przetwarzania w sekundach.
    """
    start_time = time.time()
    image = Image.open(image_path).convert('RGB')
    image_array = np.array(image)

    # Zastosowanie filtra sepii
    sepia_image_array = apply_sepia(image_array)
    sepia_image = Image.fromarray(sepia_image_array)
    sepia_image.save(save_path)

    elapsed_time = time.time() - start_time
    return elapsed_time
