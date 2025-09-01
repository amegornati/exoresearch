#!/usr/bin/env python3
"""
Convert an LSL .xdf (EEG + markers) to an MNE Raw FIF.

Usage:
  python code/convert_xdf_to_fif.py --xdf data/raw/file.xdf --out data/deriv/file_raw.fif
"""
import argparse, numpy as np, pyxdf, mne

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xdf", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    streams, header = pyxdf.load_xdf(args.xdf)
    eeg = next(s for s in streams if s['info']['type'][0] == 'EEG')
    data = np.array(eeg['time_series']).T
    sfreq = float(eeg['info']['nominal_srate'][0])
    ch_names = [c['label'][0] for c in eeg['info']['desc'][0]['channels'][0]['channel']]
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')
    raw = mne.io.RawArray(data, info)
    raw.save(args.out, overwrite=True)
    print(f"Saved FIF to {args.out}")

if __name__ == "__main__":
    main()
