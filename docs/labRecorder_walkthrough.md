# LabRecorder Walkthrough (LSL)

Goal: record synchronized EEG + event markers to a single `.xdf`.

1) Install **LabRecorder** (from LSL releases).
2) Start streams:
   - EEG (e.g., OpenBCI LSL OR `python code/sim_ssvep_lsl.py`)
   - Markers (`python stim/ssvep_stim.py`)
3) In LabRecorder:
   - Refresh streams → select **EEG** and **markers**.
   - Set filename, e.g., `data/raw/2025-09-01_S01_ssvep_01.xdf`.
4) Record (Start → run task → Stop). Confirm the file saved.
5) Analyze with your notebook or scripts.
