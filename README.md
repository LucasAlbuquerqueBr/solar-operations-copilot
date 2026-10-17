# Solar Operations Copilot

**Reproducible data preparation for solar asset performance analysis.**

An independent portfolio project built from a hackathon practice exercise using historical PVDAQ telemetry. The business question is how an operations team could prioritize investigations into underperformance while distinguishing production losses from unreliable readings.

**Current stage:** source verification and structural data profiling are implemented. Modeling, fault diagnosis, a dashboard, and financial impact estimates are planned, not delivered. This is not an official event submission or a production monitoring system.

## What you can review today

- [Interactive project map](MINDMAP.html): nested task checklists with partial progress saved locally in the browser. Open the HTML file locally after cloning; GitHub displays its source.
- [Data-quality report](data/quality/raw_profile.json): observed coverage, missing cells, timestamp counts, and sampling cadence.
- [Channel dictionary](data/metadata/channel_dictionary.csv): channel names, units, aggregation semantics, and ranges.
- [Verification and profiling pipeline](tools/verify_and_profile.py): source integrity checks and reproducible inspection.
- [Data guide](DATA_GUIDE.md): interpretation risks including daylight saving, incomplete intervals, and power versus energy.
- [Project roadmap](docs/ROADMAP.md): planned analytical and product deliverables.

The implemented work demonstrates Python/pandas data inspection, source provenance, reproducibility, and domain-aware documentation. It does not yet demonstrate predictive performance or validated maintenance recommendations.

## Dataset at a glance

Historical telemetry from PVDAQ system 2107, Farm Solar Array, California; 893 kW DC nameplate capacity. File coverage varies across 2017–2023 and does not imply continuous observations.

| Stream | Rows | Columns | Median observed interval |
|---|---:|---:|---|
| Inverter electrical readings | 632,952 | 120 | 5 minutes |
| Weather | 206,008 | 4 | 15 minutes |
| Plane-of-array irradiance | 531,019 | 2 | 5 minutes |
| Revenue-meter AC power | 240,062 | 2 | 15 minutes |

The existing structural profile records 183,372 missing numeric cells in electrical data and 156 in weather data. No invalid or duplicate local timestamps were found by that check; missing intervals, sensor accuracy, and daylight-saving ambiguities still need investigation. These are data observations, not diagnosed equipment failures.

## Run locally

Use Python 3.11 or newer. Run commands from the repository root.

```sh
python -m venv .venv
```

Activate the environment with `.venv\Scripts\Activate.ps1` on Windows PowerShell, or `source .venv/bin/activate` on macOS/Linux.

```sh
python -m pip install -r requirements.txt
python tools/download_data.py
python tools/verify_and_profile.py
python -m unittest discover -s tests -v
```

The download is about 467 MB. Valid existing files are reused. Each download must match the recorded byte count and SHA-256 before it replaces a local file. The full profile reads the largest CSV into memory; allow several GB of available RAM. Profiling regenerates the tracked dictionary and report.

Raw CSV files are intentionally excluded from Git. The local portfolio copy already contains them; a fresh clone obtains them through the downloader. Small metadata and generated inspection outputs are included for review without a download.

## Repository layout

```text
 data/          Source manifest, metadata, and structural profile
 data/raw/      Local downloads (ignored by Git)
 tools/         Download, verification, and profiling scripts
 tests/         Source-integrity tests using temporary fixtures
 docs/          Roadmap and portfolio context
 templates/     Unfilled planning templates, not analytical results
 references/    Source attribution and original exercise context
 CHALLENGE.md   Original simulated business brief and evaluation design
 DATA_GUIDE.md  Dataset semantics and limitations
```

`MINDMAP.html` provides an interactive planning checklist; it does not display analytical results. Open it directly in a browser to track tasks, steps, and individual actions. Progress is saved in that browser and is not uploaded to GitHub. `START_HERE.md` and the other HTML study pages are retained as background material. This README is the portfolio entry point.

## Design boundaries

- Preserve raw observations and verify source integrity before analysis.
- Separate missing observations from zero generation.
- Do not equate DC nameplate capacity with an AC clipping limit.
- Evaluate future models with chronological splits and report sample coverage.
- Separate observed facts, model estimates, hypotheses, and simulated assumptions.

## Source and attribution

Deline, Chris, et al. *Photovoltaic Data Acquisition (PVDAQ) Public Datasets*. NREL, 2021. DOE Open Energy Data Initiative. [DOI](https://doi.org/10.25984/1846021) · [Dataset page](https://data.openei.org/submissions/4568).

Exact source URLs, retrieval timestamps, file sizes, and checksums are preserved in [the manifest](data/download_manifest.json). Third-party data and reference documents retain their source terms; this repository does not grant a separate license for them. No project-wide license has been selected yet.

## Em português

Projeto independente de portfólio sobre preparação e auditoria de dados de uma usina solar. Já inclui verificação de integridade, perfil estrutural e documentação dos canais. Modelos, diagnóstico de falhas e interface ainda são próximos passos. O cenário comercial é simulado; os dados históricos são reais. A versão de estudo permanece separada desta cópia para publicação.

