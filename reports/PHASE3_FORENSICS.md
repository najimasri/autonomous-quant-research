# GOLDBTC-A1 Phase 3 — forensic addendum

## Scope and reproducibility

This is a text-only forensic addendum to the frozen Phase 3 result. It introduces no strategy family, configuration, evaluation, or gate change. The 128 rows were reconstructed by re-running the existing frozen family builders and Phase 3 execution/accounting functions against only the declared development and confirmation shards. `reports/phase3_forensics_tables/config_metrics.csv` is the row-level source of truth; the other CSVs are committed pivots of it except for the explicit PBO-input inventory.

The full forensic reconstruction took approximately **2,353 seconds (39 minutes 13 seconds)** of wall time in this container. This is the measured addendum reconstruction runtime, not a recovered runtime for the original Phase 3 run. The original runner contains no timer and committed no start/end timestamps, so its exact total runtime—and the time attributable only to its controls—is **not recoverable from the committed evidence**. Claiming an exact original runtime would manufacture evidence.

## Per-configuration evidence

All 128 configurations are in `config_metrics.csv`. For each row it gives development trade count; mean gross trade outcome in R before costs; mean after the base provisional cost; mean at twice the complete provisional cost; and mean after the deterministic 0.70 win haircut applied to the base-cost sequence. It also gives the configuration's development-trade median and p25 immutable stop distance in price units, the applicable round-trip price costs, gate inputs, and first failing gate.

The aggregate picture is:

| Instrument | Family | Configs | Min dev trades | Median dev trades | Gross >= 0 | Median gross R | Median base-cost R | Median 2x-cost R | Median haircut R |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | F1 | 16 | 5,872 | 11,985.0 | 4 | -0.0205 | -3.3243 | -6.6336 | -3.4157 |
| BTC | F2 | 16 | 2,279 | 34,396.5 | 13 | 0.0755 | -10.3074 | -20.6812 | -10.3232 |
| BTC | F3 | 16 | 49,077 | 106,592.5 | 8 | -0.0154 | -6.1306 | -12.2465 | -6.1580 |
| BTC | F4 | 16 | 47,833 | 128,316.0 | 16 | 0.1140 | -5.6346 | -11.3986 | -5.6909 |
| XAU | F1 | 16 | 7,526 | 15,117.5 | 6 | -0.0205 | -0.9969 | -1.9860 | -1.1717 |
| XAU | F2 | 16 | 4,547 | 53,354.0 | 8 | 0.0176 | -9.4388 | -18.8962 | -9.4638 |
| XAU | F3 | 16 | 12,097 | 61,574.0 | 5 | -0.0590 | -1.5668 | -3.0818 | -1.6425 |
| XAU | F4 | 16 | 67,993 | 188,239.0 | 16 | 0.1017 | -1.8701 | -3.8668 | -1.9593 |

Across all configurations, 76/128 had non-negative gross expectancy, but **0/128** remained non-negative after base costs, **0/128** after 2x costs, and **0/128** after the 0.70 haircut of the base-cost sequence. The respective all-config median expectancies were 0.0245 R, -4.0564 R, -8.2278 R, and -4.1301 R. These are per-trade arithmetic means, not compounded returns.

## Stop scale versus provisional costs

The price-unit round-trip base costs used by Phase 3 were BTC $70 and XAU $0.82; 2x costs were $140 and $1.64. Stop statistics are calculated across every development trade for each configuration, then the fixed instrument cost is compared with that configuration-level median and p25. The complete details are in `config_metrics.csv` and the counts are committed in `stop_cost_summary.csv`.

| Instrument | Configs | Base cost >= median stop | Base cost >= p25 stop | 2x cost >= median stop | 2x cost >= p25 stop |
|---|---:|---:|---:|---:|---:|
| BTC | 64 | **60** | **64** | **64** | **64** |
| XAU | 64 | **49** | **56** | **60** | **64** |

For context, the median across configurations of each configuration's median stop was $19.8680 for BTC and $0.5767 for XAU; the analogous p25-stop medians were $9.2541 and $0.4013. This makes the structural mismatch visible without relying on expectancy alone. XAU swap adjustments remain included in expectancy exactly as in the Phase 3 runner, but are not part of the fixed round-trip price-cost comparison above because they vary by holding nights and side.

### LOCK_A cost-contract gap

The provisional contract has BTC spread, commission, and slippage entries but **no BTC overnight swap or funding entry**. This absence is a `LOCK_A` evidence gap: the BTC cost result cannot be represented as a fully evidenced overnight carry/funding result until the operator supplies the broker/symbol contract evidence. This addendum does not invent a zero carry rate and does not change the provisional contract.

## First failing gate and kill attribution

For attribution only, gates were inspected in the evaluation order encoded by the existing `all([...])` expression: sample floor; maximum year share and minimum three contributing years (reported as separate diagnostics in the table); random-entry 95th percentile; shuffle 95th percentile; confirmation non-negative; DSR >= 0.95; haircut non-negative; 2x-cost non-negative; leave-one-year-out non-negative; corrupted-tape rejection; then family PBO <= 0.25. This ordering changes no result; it merely prevents later failures from receiving the same kill twice.

The first failing gate was `random_entry_95` for **128/128 configurations** overall and **16/16 in every family/instrument cell**. No configuration was killed first by sample quantity, year contribution, or concentration: all 128 cleared those preceding checks. The auditable overall and per-cell histogram is in `first_failing_gate_histogram.csv`. This attribution must be read alongside the control implementation disclosure below: the label “random entry” overstates what was actually computed.

## Exact control methodology

For each configuration, the original runner first calculated `len(dev)`, the observed development trade count, and read the configuration's frozen `target_r`. It seeded NumPy with `20260801 + config_id + 1000 * family_index`. It then produced 200 ensemble means; each mean came from `len(dev)` independent, equal-probability draws from exactly `[-1.0, target_r]`. It next produced another 200 means with the **same operation** and the continuing state of that RNG. The 95th percentile of each 200-mean array became `null_95` and `shuffle_95`.

Therefore:

* the “random-entry” ensemble did **not** place random entries on a tape, re-simulate exits, preserve time exposure, use observed entry opportunities, or charge trade-specific costs;
* the “shuffled-signal” control did **not** shuffle observed signals, sides, timestamps, or the realized trade sequence; and
* both controls were synthetic fair Bernoulli payoff draws with identical payoff support, differing only because the second consumed the next RNG draws.

They are neither re-simulated-entry controls nor trade-sequence operations. The original Phase 3 report's stronger “destroys the observed side/outcome pairing” characterization is not supported by the implementation. Each row's resulting thresholds are preserved in `config_metrics.csv`. As noted above, the exact original total/control runtime was not recorded; only the approximately 2,353-second full forensic reconstruction runtime is available.

## PBO inputs and the 0.0000 result

PBO was computed once per family/instrument cell from a matrix containing **all 16 configurations**, not the zero-member pre-PBO selection set. BTC matrices were 16 x 6 (six development-year expectancy columns) and yielded 20 half-split CSCV combinations. XAU matrices were 16 x 13 and yielded 1,716 combinations. For each split, the code selected the configuration with the highest mean on the chosen in-sample columns and counted a loss if that same row ranked below the midpoint among 16 rows on complementary columns. No split counted as a loss, hence 0 divided by 20 or 1,716 and the reported `0.0000`. `pbo_inputs.csv` records these actual dimensions, split counts, results, and non-empty status.

Accordingly, the **actual PBO calculation is not VACUOUS**: its input candidate matrices were non-empty. If “PBO of the pre-PBO survivors” were intended instead, all eight selection sets would be empty and such a value would be **VACUOUS / undefined**, not evidence of zero overfitting. That is not what the runner computed. Also, PBO 0.0000 does not rescue a row because the PBO gate comes after every row already failed earlier gates.

## Findings

The evidence supports **costs were structurally fatal relative to stop scale**, not trade starvation:

1. **Not starved:** the smallest development sample was 2,279 trades, every configuration met the sample floor, all 128 had at least three contributing years, and none exceeded the 0.40 single-year share before the first failure.
2. **Some merit before costs:** 76/128 configurations had non-negative gross expectancy, including all 32 F4 configurations. The all-config median gross expectancy was +0.0245 R. It is therefore inaccurate to summarize every frozen family as failing on gross merit.
3. **Costs dominate:** zero configurations had non-negative base-cost expectancy. Base round-trip cost was at least the median stop for 109/128 configurations (60 BTC + 49 XAU) and at least the p25 stop for 120/128 (64 + 56). At 2x it was at least the median for 124/128 and the p25 for 128/128.
4. **Stress confirms rather than causes the result:** the all-config median moved from +0.0245 R gross to -4.0564 R at base cost and -8.2278 R at 2x. The haircut sequence was also negative for 128/128, with median -4.1301 R, because it starts from already cost-negative trades and degrades wins.

The governed empty-set verdict remains unchanged. The forensic conclusion is narrower: the observed families were amply traded; several had weak positive gross expectancy; the provisional round-trip cost scale overwhelmed their stop scale. Because BTC carry/funding is absent and all costs remain provisional, this is a diagnosis of the frozen provisional contract—not a deployment claim and not a substitute for `LOCK_A` broker evidence.

## Committed tables

* `phase3_forensics_tables/config_metrics.csv` — all 128 configurations and requested row-level measures.
* `phase3_forensics_tables/stop_cost_summary.csv` — cost-versus-stop counts by instrument.
* `phase3_forensics_tables/first_failing_gate_histogram.csv` — overall and family/instrument kill attribution.
* `phase3_forensics_tables/pbo_inputs.csv` — actual matrix dimensions, CSCV split counts, values, and vacuity flag.
