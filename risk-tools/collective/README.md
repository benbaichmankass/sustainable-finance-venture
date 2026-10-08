# RT-7 — collective facility risk model (code)

Specification, decisions and findings: [`../rt-7-collective-facility-model.md`](../rt-7-collective-facility-model.md). Registry row: `RT-7` in `data/risk-tools.csv`.

| File | Does |
|---|---|
| `rt7_params.py` | Reads `data/rt7-parameters.csv`, `rt7-regions.csv`, `rt7-scenarios.csv`; merges shared and regional rows; validates the tracker |
| `rt7_model.py` | The model: members, one-season simulation, summaries, tornado. numpy |
| `run_region.py` | Pipeline: every region × scenario + sensitivities → `data/rt7-region-results.csv`, `data/rt7-sensitivity.csv`, per-run manifests under `output/` (gitignored) |
| `test_rt7.py` | Checks, run in CI. Includes JS/Python parity when `node` is present |
| `parity_runner.js` | Node shim that runs `dashboard/rt7-model.js` on inputs from `test_rt7.py` |
| `requirements.txt` | `numpy` |

```bash
pip install -r risk-tools/collective/requirements.txt
python3 risk-tools/collective/run_region.py
python3 risk-tools/collective/test_rt7.py
```

**Edit parameters in the CSV, not in code.** The browser tab (`dashboard/rt7-model.js`) is a port of `rt7_model.py` for interactive use; Python is the reference. If you change the model, change both and let `test_rt7.py` tell you whether they still agree.

**Nothing here is calibrated.** Every output row says `Basis: SYNTHETIC`.
