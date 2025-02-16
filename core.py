import numpy as np
from scipy import signal


UPPER_FREQUENCY = 24_000  # Maximal audio frequency.
WINDOW_INTERVAL = 0.5  # Window interval in seconds.
MIN_DISTANCE_TIME = 0.005  # Min distance between peaks in seconds.
MAX_NUM_PEAKS = 15  # Maximal number of peaks.

COMBINATORIAL_HASHING_OFFSET = 100  # Offset for creating combinatorial hashing.
MIN_TIME_IDX_HASHING_DIFF = 2
MAX_TIME_IDX_HASHING_DIFF = 10
BITS_PER_FREQUENCY = 10
BITS_PER_TIME_DIFF = 12
MAX_SCALED_FREQUENCY = 2 ** BITS_PER_FREQUENCY


def create_constellation_map(
    audio: np.ndarray, sample_rate: int
) -> list[tuple[float, int]]:
    """
        Create constellation map of the audio.
        
        Arguments:
            audio (np.ndarray): an audio for extracting constellation map.
            sample_rate (int): sample rate of the audio.
            
        Returns:
            list[tuple[int, int]]: list with tuples (freq, time_idx).
    """
    assert sample_rate <= UPPER_FREQUENCY, f'''
        Maximal frequency for audio: {UPPER_FREQUENCY}.
        Given audio with frequency: {sample_rate}.'''
    
    window_size = int(WINDOW_INTERVAL * sample_rate)
    peaks_distance = int(MIN_DISTANCE_TIME * sample_rate)
    window_size += window_size % 2
    pad_size = window_size - audio.size % window_size
    audio_padded = np.pad(audio, (0, pad_size), 'constant', constant_values=(0,))
    
    freq, time, stft = signal.stft(
        audio_padded, sample_rate, nperseg=window_size, nfft=window_size)
    
    constellation_map = []
    for time_idx, ft in enumerate(stft.T):
        peaks, properties = signal.find_peaks(np.abs(ft), distance=peaks_distance, prominence=0)
        n_peaks = min(len(peaks), MAX_NUM_PEAKS)
        peaks_idx = np.argpartition(properties['prominences'], kth=-n_peaks)[-n_peaks:]
        peak_freq = freq[peaks_idx]
        constellation_map.extend([(frequency, time_idx) for frequency in peak_freq])
    return constellation_map


def create_combinatorial_hashing(
    constellation_map: list[tuple[float, int]]
) -> dict[int, int]:
    """
        Create combinatorial hashes from constellation map.
        
        Arguments:
            constellation_map (list): constellation map of an audio.
            
        Returns:
            dict: hashes dict with mapping hash to time_idx.
    """
    hashes = {}
    for idx, (freq, time_idx) in enumerate(constellation_map):
        for other_freq, other_time_idx in constellation_map[idx + 1: idx + 1 + COMBINATORIAL_HASHING_OFFSET]:
            time_idx_diff = other_time_idx - time_idx
            if (
                time_idx_diff < MIN_TIME_IDX_HASHING_DIFF or
                MAX_TIME_IDX_HASHING_DIFF < time_idx_diff
            ):
                continue
            hash = time_idx_diff
            hash = hash | (int(freq / UPPER_FREQUENCY * MAX_SCALED_FREQUENCY) << BITS_PER_TIME_DIFF)
            hash = hash | (int(other_freq / UPPER_FREQUENCY * MAX_SCALED_FREQUENCY) << (BITS_PER_TIME_DIFF + BITS_PER_FREQUENCY))
            hashes[hash] = time_idx
    return hashes
