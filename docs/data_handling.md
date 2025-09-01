# Data Handling & Storage

**Principle:** keep **raw** data safe and out of Git; commit only small, derived outputs and code.

- `data/raw/` — raw `.xdf/.edf/.gdf` (use campus storage/VPN for backups).
- `data/deriv/` — derived `.fif`, small CSVs, QC figs.
- `fig/` — exported plots.

Naming: `YYYYMMDD_subject_task_session.ext`
Example: `20250901_S01_ssvep_01.xdf`
