# Project Cleanup Plan & Checklist

This document tracks the work needed to turn this research codebase into a clean, reproducible project that anyone on the team can run without manual path edits.

---

## Priority 1 — Make it Runnable by Anyone

These block reproducibility entirely.

- [ ] **Replace hardcoded input/output paths in all Python scripts**
  - `parse_into_dataframe_YESslices.py` — CurveAlign folder, TWOMBLI CSV, texture folders, output folder
  - `parse_into_dataframe_NOslices.py` — same paths
  - `ctfireparser.py` — input folder, output folder
  - `ctfire_statssummary.py` — input CSV path
  - `RF_regression.py` — dataframe CSV path
  - `RF_classifier.py` — dataframe CSV path
  - Strategy: add a `config.py` or use `argparse` / `pathlib` relative paths from a project root variable

- [ ] **Replace hardcoded paths in MATLAB scripts**
  - `glcm3D_attempt.m` — `folder`, `outpath`
  - `glcm3D_attempt_gpu.m` — same (also references `C:\Users\hwilson23\...`)
  - Strategy: accept folder arguments at the top of each script, or use a separate `config.m`

- [ ] **Fix the double-nested directory structure**
  - The repo root has `collagen_3D_multimetric-main/collagen_3D_multimetric-main/` — the inner folder is the actual project
  - Either flatten (move `src/`, `data/`, `docs/`, `pyproject.toml` to root) or remove the outer wrapper folder

- [ ] **Move CSV/XLSX output files to `data/` only**
  - Currently `final_dataframe_byslice_FLU_n2.csv`, `final_dataframe_byslice_SHG_n2.csv`, `finalcollapsed_dataframe_byslice_n2.csv` exist in the repo root AND in `data/` (with slightly different names)
  - Remove the root-level duplicates; standardize on one location and one naming convention

---

## Priority 2 — Code Quality

These make the code more reliable and easier to modify.

- [ ] **Remove temporary files from `data/`**
  - Delete `final_dataframe_byslice_FLU_temp.xlsx` and `final_dataframe_byslice_FLU_temp_stride5.xlsx`
  - Add `data/*.xlsx` and `data/*_temp*` to `.gitignore` to prevent future commits of scratch files

- [ ] **Add `.gitignore`**
  - Ignore: `*.xlsx`, `*.mat`, `__pycache__/`, `.ipynb_checkpoints/`, `*.pyc`, large generated TIF outputs

- [ ] **Make column dropping in ML scripts data-driven**
  - `RF_regression.py` and `RF_classifier.py` drop columns by hardcoded name list
  - Replace with: drop non-numeric columns, or columns matching a pattern, so renames upstream don't silently break the model

- [ ] **Standardize output file naming**
  - The `_n2` suffix on the root-level CSVs vs. no suffix in `data/` is confusing
  - Decide on one convention and document it (e.g., version suffix only when a dataset is frozen for a paper figure)

- [ ] **Add docstrings to the main functions in Python scripts**
  - Priority: `reshape_CA()`, `twombli_slice_data()`, `process_img_folder()`, `find_identical_columns()`, `collapse_identical_columns()`
  - One-line description + parameter list is sufficient

---

## Priority 3 — Project Structure

These improve navigability without changing behavior.

- [ ] **Add a top-level `README.md` that links to `docs/`**
  - The current `README.md` at the project root mixes the Python pipeline and GLCM documentation in one flat file
  - Rewrite as a short project intro that links to `docs/OVERVIEW.md` and the subproject docs

- [ ] **Add a `scripts/` or top-level entry points**
  - Create a single `run_pipeline.py` (or shell script) that calls the parse and ML scripts in order with sample paths
  - This gives a newcomer one command to run to reproduce results

- [ ] **Consolidate `parse_into_dataframe_YESslices.py` and `NOslices.py`**
  - The two files share >80% of their code
  - Refactor into one script with a `--per-slice` / `--per-stack` flag, or a shared `pipeline.py` module with a `main()` that both call

- [ ] **Move notebook to a dedicated `notebooks/` folder**
  - `analyze_dataframe.ipynb` currently lives in `src/collagen_dataframe/`
  - Notebooks are not source code — move to `notebooks/` at project root level

---

## Priority 4 — Reproducibility & Environment

- [ ] **Add a `README` section on how to run**
  - Required software versions (MATLAB version, Python version)
  - Step-by-step: install dependencies → run GLCM MATLAB → run Python pipeline → run ML scripts
  - How to point scripts at your own data

- [ ] **Pin MATLAB toolbox versions in documentation**
  - Note which MATLAB release was tested (R20XXa/b)

- [ ] **Add a sample/test dataset or point to one**
  - The `ground_truth_data/` spiral TIFs are perfect for a smoke test
  - Document: "run the pipeline on these files to verify your installation"

- [ ] **Consider adding a `Makefile` or `justfile` for common tasks**
  - `make pipeline` → runs parse scripts
  - `make ml` → runs RF scripts
  - `make clean` → removes generated CSVs and plots

---

## Summary of File Changes

| Action | Files |
|---|---|
| Delete duplicates | Root-level `*_n2.csv` files (keep `data/` copies) |
| Delete temp files | `data/*_temp*.xlsx`, `data/*_stride5*` |
| Add | `.gitignore` |
| Add | `config.py` (or `argparse` in each script) |
| Add | `scripts/run_pipeline.py` |
| Move | `analyze_dataframe.ipynb` → `notebooks/` |
| Rewrite | Root `README.md` (shorter, link to docs) |
| Refactor | `parse_into_dataframe_YESslices.py` + `NOslices.py` → shared module |
