# Methodology — REINS Resourcing Metrics

This document explains, in detail, how REINS turns three flat tables — a trial
portfolio, a resource roster, and an allocation list — into the utilization,
staffing-mix, and per-trial breakdown numbers on screen. It covers the
definitions, the precedence rules, and the limitations.

The entire metrics layer lives in one place:

- `app/state.py` — every KPI, chart series, and table is a reactive
  `@rx.var` computed over the in-memory tables. There is **no stored
  aggregate**: change a filter or select a different trial and everything
  downstream recomputes. This keeps one definition of "utilization" (etc.) for
  the whole app instead of scattering the math across pages.

The domain and the shape of the three input tables are described separately in
[`DATA_MODEL.md`](DATA_MODEL.md).

---

## 1. Inputs and loading

Three CSVs are read into state on app load (`AppState.on_load`), plus three more
used by the site and roster views:

- **`Trial.csv`** — one row per study (`protocol_id`, `phase`,
  `therapeutic_area`, `status`, `priority`, `sites_count`, …).
- **`Resource.csv`** — one row per person (`name`, `type` = FTE/FSP/Contractor,
  `role`, `department`, `capacity` in weekly hours, `utilization` %).
- **`Allocation.csv`** — one row per (person × study) booking
  (`trial_id`, `resource_id`, `weekly_hours`, `allocation_percentage`,
  `start_date`, `end_date`).

Loading is deliberately defensive: only known columns are kept, numeric fields
(`utilization`, `capacity`, `weekly_hours`, `allocation_percentage`) are coerced
with `pd.to_numeric(..., errors="coerce").fillna(0)`, and a missing file yields
an empty frame rather than an exception. This is what lets the same code run
against a different portfolio without edits.

---

## 2. The join model

Two joins drive everything:

- **Allocation → Trial** on `Allocation.trial_id == Trial.protocol_id`
  (the allocation's study reference is the protocol id, e.g. `RSP-2024-004`).
- **Allocation → Resource** on `Allocation.resource_id == Resource.name`.

> **Known limitation — name-based resource keys.** Allocations currently
> reference a person by *name* (e.g. `"Dr. Emily Rodriguez"`), not a stable id.
> The roster view normalizes names before joining (`_norm_name`: lower-case,
> strip titles like *Dr./Mr./Prof.*, drop punctuation) to make the match robust
> to formatting, and the code is structured to prefer a real identifier
> (`NTID / Network ID / Employee ID`) the moment the data carries one. Until
> then, two different people with the same normalized name would collide. This
> is the single most important data-quality upgrade on the roadmap.

---

## 3. Utilization

Utilization is the load a person carries relative to their capacity. REINS
computes it two ways for two different questions.

### 3.1 Portfolio-level average (`avg_util`)

The headline "average utilization" KPI is the simple mean of the `utilization`
column across all resources currently in view:

```
avg_util = mean(Resource.utilization over resources)
```

It is then banded for the sub-label:

| Band | Condition |
|---|---|
| **Underutilized** | `avg_util < 30` |
| **Balanced workload** | `30 ≤ avg_util ≤ 70` |
| **High load** | `avg_util > 70` |

This uses the roster's self-reported utilization directly — it is a roster-health
readout, independent of any single trial.

### 3.2 Per-resource utilization for a selected trial (`_per_resource_util_list`)

When a trial is selected in Portfolio, REINS re-derives utilization *from the
allocations* so the number reflects real bookings, not the roster field. For each
resource allocated to the trial it aggregates hours and percent across that
resource's allocation rows, then picks a value by **precedence**:

```
if weekly_hours are present AND capacity > 0:
    util% = (Σ weekly_hours / capacity) × 100        # hours-based (preferred)
elif allocation_percentage is present:
    util% = Σ allocation_percentage                  # percent-based
else:
    util% = Resource.utilization                     # roster fallback
util% = max(0, util%)
```

The precedence matters: hours ÷ capacity is the most honest measure, but if a
dataset only carries allocation percentages the metric degrades gracefully to
those, and only falls back to the static roster figure when neither is present.

From that per-resource list the app derives:

- **`selected_avg_util`** — mean utilization across the trial's resources.
- **`selected_overallocated`** — count of resources with `util > 100%`.
- **`selected_underutilized`** — count with `util < 30%`.

---

## 4. Staffing mix (FTE / FSP)

REINS treats staffing as a two-way split: **FTE** (badged employees) vs.
**FSP / Contractor** (functional-service-provider and contract staff, bucketed
together). Anything not explicitly `FTE` is counted on the FSP side.

**Portfolio ratio** (`fte_share` / `fsp_share`), over the resource roster:

```
fte_share = round(100 × FTE_count / (FTE_count + FSP_count))
fsp_share = 100 − fte_share
```

**Per-trial split** (`selected_type_counts` → `selected_fte_pct`): the same
FTE-vs-rest bucketing, but restricted to the resources allocated to the selected
trial, and rendered as a donut via a CSS `conic-gradient` (a 1% white gap
separates the two arcs).

---

## 5. Per-trial breakdowns

With a trial selected, three rollups describe *how* it is staffed. All three
convert each allocation to an **hours** figure with one shared rule, then group.

**Hours per allocation** (preference order):

```
hours = weekly_hours                                 # if present
      = (allocation_percentage / 100) × capacity     # else, if both present
      = 0                                             # otherwise (skipped)
```

- **Functional-area breakdown** (`selected_functional_breakdown`) — hours rolled
  up by the resource's `role`, sorted descending, then converted to percentages
  and colors for the pie legend.
- **Department breakdown** (`selected_department_breakdown`) — the same hours,
  rolled up by `department`; also surfaced as chart data.
- **Resource detail table** (`selected_resources_detail`) — one row per
  allocated resource with name, role, type, department, aggregated weekly hours,
  allocation %, and the min-start / max-end **date range** across their
  allocation rows. Where one of hours/percent is missing it is back-derived from
  the other via capacity, so the table is always complete. Sorted by allocation
  % descending.

---

## 6. Filtering

The Portfolio trial list is the product of five independent, composable filters
(`filtered_trials`): a free-text **search** over title and protocol id, plus
exact-match **status**, **phase**, **priority**, and **therapeutic area**. Each
filter's option list is derived reactively from the data actually present
(`*_options` vars), so the dropdowns never offer a value the portfolio doesn't
contain. Every KPI in §3–§5 is computed over the *filtered* set, so narrowing to,
say, Oncology reflows the entire dashboard to that slice.

`filtered_trials_with_counts` additionally attaches a distinct **resource count**
per trial by grouping allocations by study.

---

## 7. Parameters & thresholds

| Parameter | Value | Meaning |
|---|---|---|
| Underutilized threshold | `< 30%` | flags a resource / bands the portfolio average |
| Balanced band | `30–70%` | healthy portfolio-average utilization |
| High-load threshold | `> 70%` | portfolio average; per-resource over-allocation is `> 100%` |
| FTE bucket | `type == "FTE"` | everything else counts as FSP / Contractor |
| Hours source precedence | `weekly_hours` → `%×capacity` → roster `utilization` | see §3.2, §5 |

---

## 8. Limitations & possible extensions

- **Name-based joins (see §2).** Moving allocations and roster onto stable
  employee identifiers (NTIDs) is the top data-quality item; the join code
  already prefers an id when present.
- **Static utilization is a snapshot, not a schedule.** Utilization today is a
  single scalar per resource/allocation. Because allocations carry
  `start_date`/`end_date`, a natural extension is a **time-phased** utilization
  curve — load per week over the study calendar — which is the foundation for
  the capacity-planning feature below.
- **Capacity planning / simulation (roadmap).** The intended next step is to
  forward-simulate *demand for people* as studies ramp (enrollment and site
  activation drive monitoring and data-management load) against roster
  **supply**, flagging where and when a function will be short-staffed — the
  people-side analogue of a supply-stockout forecast. The Resources view already
  scaffolds `open_positions` / `capacity_planning` / `incoming` tabs for this.
- **Home pipeline counts are illustrative.** The phase-count tiles and
  therapeutic-area focus board on Home are currently seeded constants, not yet
  derived from `Trial.csv`; wiring them to `phase_options` / `area_options` is a
  small, well-scoped change.
- **Analytics & Timeline pages are placeholders.** The metrics layer already
  exposes the series (utilization distribution, department hours, type split)
  these pages need; they await their charts.
- **No persistence.** Data is read-only from CSV each load. A database-backed
  version (the requirements already include SQLAlchemy / SQLModel via Reflex)
  would allow editing allocations and seeing utilization update live.

---

## 9. Data sources

In a production deployment these tables would be extracted from the CTMS /
resource-management systems of record. The committed `app/data/` CSVs are
**synthetic** stand-ins — invented trials, people, and allocations — so the tool
runs end-to-end without access to any real system or personnel data.
