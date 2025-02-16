import numpy as np
from scipy import signal


WINDOW_INTERVAL = 0.5  # Window interval in seconds.
MIN_DISTANCE_TIME = 0.005  # Min distance between peaks in seconds.
MAX_NUM_PEAKS = 15  # Maximal number of peaks.


def create_constellation_map(
    audio: np.ndarray, sample_rate: int
) -> list[tuple[int, int]]:
    """
        Create constellation map of the audio.
        
        Arguments:
            audio (np.ndarray): an audio for extracting constellation map.
            sample_rate (int): sample rate of the audio.
            
        Returns:
            list[tuple[int, int]]: list with tuples (freq, time_idx).
    """
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
