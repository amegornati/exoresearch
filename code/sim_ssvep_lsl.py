#!/usr/bin/env python3
"""
Publish a synthetic EEG LSL stream that contains SSVEP components at 10/12/15/20 Hz plus noise.
Use to test pipeline with no hardware.

Run:
  python code/sim_ssvep_lsl.py
"""
import numpy as np, time
from pylsl import StreamInfo, StreamOutlet

FS = 256
N_CH = 4
CHAN_NAMES = ["Fz","Cz","Pz","Oz"]
FREQS = [10,12,15,20]
NOISE = 0.5
AMP   = 1.5

def main():
    info = StreamInfo('EEG', 'EEG', N_CH, FS, 'float32', 'sim_ssvep_001')
    ch = info.desc().append_child("channels")
    for n in CHAN_NAMES:
        ch.append_child("channel").append_child_value("label", n)
    outlet = StreamOutlet(info)

    print("Sim EEG LSL stream 'EEG' at 256 Hz. CTRL+C to stop.")
    t0 = time.time()
    t = 0
    dt = 1.0/FS
    while True:
        sample = np.zeros(N_CH, dtype=np.float32)
        for ch_idx in range(N_CH):
            for f in FREQS:
                amp = AMP * (1.0 if ch_idx == N_CH-1 else 0.4)  # stronger on Oz
                sample[ch_idx] += amp * np.sin(2*np.pi*f*t)
            sample[ch_idx] += NOISE*np.random.randn()
        outlet.push_sample(sample.tolist())
        t += dt
        # maintain ~FS
        time.sleep(max(0, t0 + t - time.time()))

if __name__ == "__main__":
    main()
