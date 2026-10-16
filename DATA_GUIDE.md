# Data guide

## Original downloads

| File in data/raw | Rows | Columns | Observed coverage | Median timestamp step |
|---|---:|---:|---|---|
| 2107_electrical_data.csv | 632,952 | 120 | 2017-11-01 to 2023-11-07 | 5 minutes |
| 2107_environment_data.csv | 206,008 | 4 | 2017-12-01 to 2023-10-31 | 15 minutes |
| 2107_irradiance_data.csv | 531,019 | 2 | 2017-11-01 to 2023-11-01 | 5 minutes |
| 2107_meter_15m_data.csv | 240,062 | 2 | 2017-01-01 to 2023-11-09 | 15 minutes |

Counts include timestamp columns. These ranges and medians were computed from the downloaded files, not inferred from their names. They do not imply continuous coverage. All four files parsed successfully; the initial audit found no invalid or duplicated local timestamps. Missing timestamps, daylight-saving ambiguities, implausible values, and cross-stream alignment still require investigation.

The electrical file contains 183,372 missing numeric cells; the weather file contains 156. The irradiance and meter files have no explicit missing cells, but omitted timestamps can still represent missing observations. See `data/quality/raw_profile.json` for exact endpoints and year counts.

## Channel dictionary

`data/metadata/channel_dictionary.csv` maps each downloaded column to original metadata, including units, aggregation type, missing count, and raw range. `2107_system_metadata.json` remains the authoritative downloaded site metadata, although it has limitations.

| Channel | Meaning | Source unit |
|---|---|---|
| measured_on | Local instrument timestamp | PST8PDT / US Pacific context |
| meter_revenue_grade_ac_output_meter_149578 | Site revenue-meter AC power | kW |
| poa_irradiance_o_149574 | Irradiance in the plane of the panels | W/m² |
| ambient_temperature_o_149575 | Ambient temperature | °F |
| wind_speed_o_149576 | Wind speed | mph |
| wind_direction_o_149577 | Wind direction | degrees |
| inv_XX_ac_power_* | Individual inverter AC power | kW |
| inv_XX_dc_current_* / dc_voltage_* | DC current / voltage | A / V |
| inv_XX_ac_current_* / ac_voltage_* | AC current / voltage | A / V |

Do not confuse power with energy: the revenue-meter channel is average power in kW, despite being described as a meter output. Fahrenheit converts to Celsius as `(F - 32) × 5 / 9`; mph converts to m/s as `mph × 0.44704`.

## Real data issues to investigate

1. **Metadata coverage mismatch.** The JSON system summary lists a first timestamp in December 2018, but the CSVs contain 2017 data. Preserve both facts; use observed file coverage for the split and document the discrepancy.
2. **Channel naming.** Inverter 15 AC power is named `inv_15_ac_power_iinv_149653` in the electrical CSV. Do not lose it through a pattern that assumes every name uses `_inv_`. The electrical file also lacks inverter 05 DC voltage. Do not manufacture it.
3. **Capacity.** 893 kW is DC nameplate capacity, not the AC clipping threshold. Determine appropriate inverter comparisons from their own available metadata and observed behavior.
4. **Time alignment.** Equipment metadata marks intervals `L` (left aligned). Treat this as the documented convention and validate it against measurements; start-of-file times alone are not enough to establish interval meaning. Do not shift streams merely to improve a score.
5. **Daylight saving.** Local timestamps have no explicit UTC offset. A lack of duplicates does not establish how the acquisition system handled repeated clock hours. State and test a policy; do not assume a fixed UTC-8 offset year-round.
6. **Coverage.** A fifteen-minute electrical average should track the expected three five-minute samples. An interval supported by one sample is not equivalent to a complete interval. Track coverage per stream before joining.
7. **Semantics.** Weather wind channels are marked as samples, whereas power and irradiance channels are averages. Wind direction requires circular treatment if aggregating across multiple directions.

## Practical starting point

Start with January through June 2021 to learn the schema and build charts. For model fitting and final evaluation, return to the training/validation/test rules in `CHALLENGE.md`.

Read selected columns from the electrical file if memory is limited. Join on explicit time intervals, not row order. Keep original local timestamps alongside any derived UTC timestamps and flags. Avoid interpolation across long outages, and do not interpolate final-test targets.

The downloaded data has not been cleaned, resampled, joined, or labeled with failures. The supplied profile is structural inspection, not certification of sensor accuracy.

## Provenance and attribution

Source: Deline, Chris, et al. *Photovoltaic Data Acquisition (PVDAQ) Public Datasets*. NREL, 2021. DOE Open Energy Data Initiative. DOI: https://doi.org/10.25984/1846021.

Dataset page: https://data.openei.org/submissions/4568

Selected source prefix: `s3://oedi-data-lake/pvdaq/2023-solar-data-prize/2107_OEDI/`

Downloaded October 15, 2026 (America/Los_Angeles). Exact UTC retrieval times, URLs, byte counts, and SHA-256 hashes are in `data/download_manifest.json`. Keep attribution and consult the license link on the source page before redistributing. The May 2026 official change log is included for source-history context; it does not mean every file was revised on that date.
