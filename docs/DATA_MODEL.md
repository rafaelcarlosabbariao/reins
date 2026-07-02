# Data Model — the clinical-resourcing domain

REINS models one question: **do we have the right people, in the right functions,
allocated at the right level, to run this portfolio of trials?** Answering it
cleanly requires only a handful of entities and the relationships between them.
This document describes that domain model — the conceptual companion to the
computation rules in [`METHODOLOGY.md`](METHODOLOGY.md).

![Data model](assets/data_model.svg)

---

## 1. The six entities

| Entity | File | Grain | Key fields |
|---|---|---|---|
| **Trial** | `Trial.csv` | one study | `protocol_id`, `phase`, `therapeutic_area`, `status`, `priority`, `budget`, `sites_count`, `enrollment_target` |
| **Resource** | `Resource.csv` | one person | `name`, `type` (FTE/FSP/Contractor), `role`, `department`, `capacity` (weekly hrs), `utilization` (%) |
| **Allocation** | `Allocation.csv` | one person × study booking | `trial_id`, `resource_id`, `allocation_percentage`, `weekly_hours`, `start_date`, `end_date` |
| **Site** | `Site.csv` | one trial site | `trial_id`, `site_id`, `country`, `city`, `principal_investigator`, `enrollment_target`, `enrolled_count`, lat/long |
| **Site Allocation** | `SiteAllocation.csv` | one person × site booking | `site_id`, `resource_id`, `allocation_percentage`, `weekly_hours`, `role_at_site` |
| **Open Position** | `OpenPosition.csv` | one unfilled req | `title`, `functional_group`, `level`, `type`, `status`, `priority`, `required_skills`, `target_fill_date` |

The three the dashboard is built on today are **Trial**, **Resource**, and
**Allocation**; Site / Site Allocation / Open Position extend the same model
toward site-level staffing and the hiring pipeline.

## 2. How they relate

```
Trial  1 ──< Allocation >── 1  Resource        "who is booked on what, and how much"
  │                               │
  │ 1                             │ 1
  ∧                               ∧
Site   1 ──< SiteAllocation >── 1 Resource       "who is booked at which site"

Open Position ── (fills into) ──> Resource        "the gap the roster doesn't cover yet"
```

- **Allocation** is the associative entity at the center: a many-to-many bridge
  between Trials and Resources carrying the *amount* of the booking
  (percent and/or weekly hours) and its *window* (start/end). Almost every metric
  in the app is an aggregation over Allocation, grouped one way or another.
- A **Resource** rolls up into two categorical hierarchies that the breakdowns
  pivot on: **functional area** (`role`) and **department**. The FTE-vs-FSP
  **type** is the third categorical axis.
- **Capacity** (a resource's weekly-hour ceiling) is what turns a raw booking
  into a *utilization*: hours booked ÷ capacity. Without capacity you have
  activity; with it you have load.

## 3. Why an associative model, not a spreadsheet

The instinct is to keep resourcing in one wide sheet — a row per person with a
column per study. That breaks the moment a person is on three studies with
different percentages and date ranges, and it can't answer "how is *this* trial
staffed by department." Splitting the booking into its own **Allocation** entity
makes both directions cheap:

- **By trial** → filter Allocation to one `trial_id`, join to Resource, group by
  role / department / type. (This is the Portfolio per-trial breakdown.)
- **By person** → filter Allocation to one `resource_id`, list the trials.
  (This is the Resources allocations panel.)

Same table, two lenses, no duplicated truth.

## 4. Identity and the join key

The clean version of this model joins on stable identifiers: `Allocation.trial_id
→ Trial.protocol_id` and `Allocation.resource_id → Resource.<employee id>`. The
trial join already works this way. The **resource** join currently keys on
*name*, normalized to survive formatting differences (titles stripped,
lower-cased, de-punctuated). The code is written to prefer a real id
(`NTID / Network ID / Employee ID`) as soon as the data carries one — see
§2 of [`METHODOLOGY.md`](METHODOLOGY.md) for why this is the model's most
important hardening step.

## 5. From model to screen

Every view is this model under a different `group by`:

| View | Grouping |
|---|---|
| Portfolio KPIs | Trial (filtered) + Resource roster |
| Functional-area pie | Allocation → Resource.`role`, summing hours |
| Department breakdown | Allocation → Resource.`department`, summing hours |
| FTE/FSP donut | Resource.`type`, counting |
| Per-resource table | Allocation grouped by `resource_id` |
| Resources panel | Allocation grouped by person, listed by trial |

The model is small on purpose. The value isn't in the schema's size — it's in
having **one** place where a trial, a person, and a booking mean exactly one
thing, so every number the app shows traces back to the same source of truth.
