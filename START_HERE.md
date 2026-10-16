# Solar Operations Copilot — Hackathon Preparation

Build a prototype that helps a solar asset manager find underperforming equipment, distinguish suspicious readings from production losses, and decide what to investigate first.

**This is an independently designed practice challenge, not an official Stanford or sponsor challenge.** Everything in this package is in English. The measurements are real US PVDAQ data; the client, business assumptions, tasks, time budget, and judging rubric are simulated.

## Start in this order

1. Read `CHALLENGE.md` for the business problem, required tasks, and evaluation.
2. Read `DATA_GUIDE.md` before joining or interpreting the measurements.
3. Inspect `data/metadata/channel_dictionary.csv` and the original JSON metadata.
4. Work from the four original files in `data/raw/`. Start with meter, irradiance, and weather; add inverter data for diagnosis.
5. Use `templates/` to structure your submission. Save your own analysis and prototype in a new `solution/` folder.

## What is included

- Four original CSV datasets: electrical telemetry, weather, plane-of-array irradiance, and revenue-meter power.
- Original metadata for system 2107, Farm Solar Array, Arbuckle, California: 893 kW DC, fixed ground mount, 24 inverter AC-power channels in the downloaded electrical file.
- Approximately 466.6 MB of original data and metadata (decimal MB). Different files cover different portions of 2017–2023.
- Official PVDAQ documentation and the May 2026 Solar Data Prize change log.
- A download manifest with exact source URLs, byte counts, retrieval times, and SHA-256 checksums.
- A generated channel dictionary and structural data-quality profile.
- An English challenge, delivery templates, and simulated judging criteria.

All datasets needed for the core challenge are local. No API key, external weather download, or paid service is necessary. We selected one complete historical site bundle rather than the entire multi-site PVDAQ archive. Later 2024/2025 extensions and the duplicate `_v1` electrical file were intentionally excluded to keep the historical benchmark fixed and avoid overlapping versions.

## Optional verification

Requires Python and pandas. From this folder:

```powershell
python -m pip install -r requirements.txt
python tools/verify_and_profile.py
```

The script checks downloaded source hashes and regenerates the dictionary and structural profile. It does not clean the measurements, train a model, or solve the challenge.

## Event alignment

The linked event is **Cleantech Hackathon at Stanford**, scheduled for October 23–24, 2026, at the Jen-Hsun Huang Engineering Center. Its public description emphasizes practical prototypes addressing business challenges from sponsors and the Stanford Sustainability Accelerator. The page lists TotalEnergies, Silicon Valley Clean Energy, and SE Ventures among its sponsors. Its detailed hackathon guide was still marked as forthcoming when checked on October 15, 2026.

That supports practicing a useful product with a credible operational and commercial case. It does not confirm that solar analytics, PVDAQ, these tasks, or this rubric will appear at the event. See `references/EVENT_AND_SOURCES.md`.
