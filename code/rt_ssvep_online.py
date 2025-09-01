#!/usr/bin/env python3
"""
Real-time SSVEP decoder from an LSL EEG stream.

- Resolves the first LSL stream of type 'EEG'
- Computes band power around target frequencies over a sliding window
- Prints live decisions and emits 'decision:<label>' markers

Config: see config/config.yaml
"""
import time, yaml, collections
from pathlib import Path
import numpy as np
from scipy.signal import welch
from pylsl import StreamInfo, StreamOutlet
from utils.lsl_utils import resolve_first_inlet, make_marker_outlet, push_marker

# Load config relative to the repo root (../config/config.yaml)
CFG_PATH = Path(__file__).resolve().parents[1] / "config" / "config.yaml"
with open(CFG_PATH, "r", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

print(f"[RT] Loading config from: {CFG_PATH}")

FREQS = CFG["frequencies_hz"]
LABELS = CFG["labels"]
WIN = CFG["window_sec"]
STEP = CFG["step_sec"]
BW = CFG["bandwidth_hz"]
EEG_TYPE = CFG["lsl"]["eeg_stream_type"]
FS_FALLBACK = CFG["eeg"]["expected_sampling_rate"]

def band_power(psd_f, psd_pxx, f0, bw):
    idx = (psd_f >= (f0 - bw)) & (psd_f <= (f0 + bw))
    return np.trapz(psd_pxx[idx], psd_f[idx])

def main():
    eeg_inlet = resolve_first_inlet("type", EEG_TYPE)
    fs = int(eeg_inlet.info().nominal_srate() or FS_FALLBACK)
    n_ch = eeg_inlet.info().channel_count()
    print(f"[RT] Connected to EEG stream: fs={fs}Hz, n_ch={n_ch}")

    out = make_marker_outlet(name="decisions")

    buf_len = int(WIN * fs)
    hop = int(STEP * fs)
    ring = collections.deque(maxlen=buf_len)

    # Fill buffer
    while len(ring) < buf_len:
        sample, _ = eeg_inlet.pull_sample(timeout=1.0)
        if sample is not None:
            ring.append(sample)

    last_print = time.time()
    while True:
        # Read hop samples
        for _ in range(hop):
            sample, _ = eeg_inlet.pull_sample(timeout=1.0)
            if sample is not None:
                ring.append(sample)
        X = np.array(ring)  # [buf_len, n_ch]
        sig = X[:, -1]      # last channel (Oz-ish) by default

        f, pxx = welch(sig, fs=fs, nperseg=min(512, len(sig)))
        powers = [band_power(f, pxx, f0, BW) for f0 in FREQS]
        k = int(np.argmax(powers))
        decision = LABELS[k]

        now = time.time()
        if now - last_print >= STEP:
            print(f"Decision: {decision} | powers={['%.3f'%p for p in powers]}")
            push_marker(out, f"decision:{decision}")
            last_print = now

if __name__ == "__main__":
    main()
