# app/state.py
from __future__ import annotations
import reflex as rx
from datetime import date
from pathlib import Path
from typing import Optional, List, Dict
import pandas as pd
import re

def _type_style(t: str) -> tuple[str, str, str]:
    """Return (label, color, bg) for a given type string."""
    label = (t or "").strip()
    key = label.upper()
    color_map = {"FTE": "#2563EB", 
                 "FSP": "#10B981", 
                 "CONTRACTOR": "#A78BFA"}
    bg_map    = {
        "FTE": "rgba(37,99,235,0.12)",
        "FSP": "rgba(16,185,129,0.12)",
        "CONTRACTOR": "rgba(167,139,250,0.16)",
    }
    return label, color_map.get(key, "#64748B"), bg_map.get(key, "rgba(100,116,139,0.12)")

def _norm_name(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"^(dr|mr|mrs|ms|miss|prof)\.?\s+", "", s)   # drop titles
    s = re.sub(r"[^a-z\s]", "", s)                         # rm punct
    s = re.sub(r"\s+", " ", s)
    return s

def _first(d: dict, keys: list[str]) -> str:
    for k in keys:
        # case-insensitive column match
        for dk in d.keys():
            if dk.lower() == k.lower():
                v = d.get(dk)
                return "" if v is None else str(v).strip()
    return ""

class AppState(rx.State):
    # ---------- Filters ----------
    query: str = ""
    phase: str = "All"
    priority: str = "All"
    therapeutic_area: str = "All"
    status: str = "All"
    department: str = "All"

    # ---------- Data in memory ----------
    trials: List[Dict] = []
    resources: List[Dict] = []
    allocations: List[Dict] = []

    # ---------- Selection for Trials panel ----------
    selected_trial_id: Optional[str] = None

    # ---------- Home Page ----------
    pipeline_snapshot_asof: str = date.today().strftime("%B %d, %Y")
    phase_counts: list[dict] = [
        {"label": "Phase 1", "phase": "P1", "value": 9},
        {"label": "Phase 2", "phase": "P2", "value": 8},
        {"label": "Phase 3", "phase": "P3", "value": 7},
        {"label": "Registration", "phase": "REG", "value": 2},
    ]

    # Sidebar resource ratios
    fte_pct: int = 60
    fsp_pct: int = 40

    @rx.var
    def phase_total(self) -> int:
        return sum(int(x.get("value", 0)) for x in self.phase_counts)

    therapeutic_areas: list[dict] = [
        {"title": "Internal Medicine", "count": 6, "img": "/ta/internal_medicine.png", "href": "/portfolio?ta=IM"},
        {"title": "Inflammation & Immunology", "count": 5, "img": "/ta/inflammation_and_immunology.png", "href": "/portfolio?ta=I&I"},
        {"title": "Vaccines", "count": 6, "img": "/ta/vaccines.png", "href": "/portfolio?ta=Vaccines"},
        {"title": "Oncology", "count": 7, "img": "/ta/oncology.png", "href": "/portfolio?ta=Oncology"},
    ]

    # ---------- Load data (CSV) ----------
    def on_load(self):
        """Load datasets from app/data first, then known fallbacks."""
        candidates = [
            Path("app/data"),
            Path("data"),
            # repo-local fallback you specified
            Path("/mnt/data/reins_reflex/reins_reflex/app/data"),
            # original React upload fallback (kept for dev convenience)
            Path("/mnt/data/reins_js/reins_js/src/data"),
        ]
        data_dir = next((p for p in candidates if p.exists()), None)

        def safe_csv(name: str) -> pd.DataFrame:
            if not data_dir:
                return pd.DataFrame()
            p = data_dir / name
            if not p.exists():
                return pd.DataFrame()
            try:
                return pd.read_csv(p)
            except Exception:
                return pd.DataFrame()

        t = safe_csv("Trial.csv")
        r = safe_csv("Resource.csv")
        a = safe_csv("Allocation.csv")

        # Trials
        if not t.empty:
            keep_t = [
                "id", "title", "protocol_id", "phase", "therapeutic_area", "status",
                "start_date", "end_date", "fte_allocation", "fsp_allocation",
                "priority", "sites_count",
            ]
            self.trials = t[[c for c in keep_t if c in t.columns]].fillna(0).to_dict("records")
        else:
            self.trials = []

        # Resources
        if not r.empty:
            allowed_r = ["id", "name", "type", "role", "utilization", "capacity", "department"]
            cols = [c for c in allowed_r if c in r.columns]
            df_r = r[cols].copy()
            # numeric coercion only when present
            for num in ("utilization", "capacity"):
                if num in df_r.columns:
                    df_r[num] = pd.to_numeric(df_r[num], errors="coerce").fillna(0.0)
            if "id" in df_r.columns:
                df_r["id"] = df_r["id"].astype(str)
            self.resources = df_r.to_dict("records")
        else:
            self.resources = []

        # Allocations
        if not a.empty:
            allowed_a = [
                "trial_id", "protocol_id", "resource_id",
                "weekly_hours", "allocation_percentage",
                "role", "type", "start_date", "end_date",
            ]
            cols = [c for c in allowed_a if c in a.columns]
            df_a = a[cols].copy()
            # numeric coercion only when present
            for num in ("weekly_hours", "allocation_percentage"):
                if num in df_a.columns:
                    df_a[num] = pd.to_numeric(df_a[num], errors="coerce").fillna(0.0)
            # stringify ids
            for idc in ("trial_id", "protocol_id", "resource_id"):
                if idc in df_a.columns:
                    df_a[idc] = df_a[idc].astype(str)
            self.allocations = df_a.to_dict("records")
        else:
            self.allocations = []

        # No default trial selected 
        self.selected_trial_id = None

    # ---------- Actions / Event Handlers ----------
    # explicit setters (and aliases) - avoids set_* vs set_*_ collisions
    def set_status(self, value: Optional[str]):
        self.status = value

    def set_phase(self, value: Optional[str]):
        self.phase = value

    def set_priority(self, value: Optional[str]):
        self.priority = value

    def set_therapeutic_area(self, value: Optional[str]):
        self.therapeutic_area = value

    def set_department(self, value: Optional[str]):
        self.department = value

    def set_query(self, value: Optional[str]):
        self.query = value

    def select_trial(self, trial_id: str):
        self.selected_trial_id = str(trial_id)

    def clear_selection(self):
        self.selected_trial_id = None

    # ---------- Options (reactive lists) ---------- 
    @rx.var
    def status_options(self) -> List[str]:
        if not self.trials:
            return ["All"]
        vals = {str(t.get("status")) for t in self.trials if t.get("status")}
        return ["All"] + sorted(v for v in vals if v and v != "0")
    
    @rx.var
    def phase_options(self) -> List[str]:
        if not self.trials:
            return ["All"]
        vals = {str(t.get("phase")) for t in self.trials if t.get("phase")}
        return ["All"] + sorted(v for v in vals if v and v != "0")
    
    @rx.var
    def priority_options(self) -> List[str]:
        if not self.trials:
            return ["All"]
        vals = {str(t.get("priority")) for t in self.trials if t.get("priority")}
        return ["All"] + sorted(v for v in vals if v and v != "0")
    
    @rx.var
    def area_options(self) -> List[str]:
        if not self.trials:
            return ["All"]
        vals = {str(t.get("therapeutic_area")) for t in self.trials if t.get("therapeutic_area")}
        return ["All"] + sorted(v for v in vals if v and v != "0")
    
    @rx.var
    def department_options(self) -> List[str]:
        if not self.trials:
            return ["All"]
        # Only populate if the dataset has 'department'; otherwise return just All
        if self.trials and "department" in self.trials[0]:
            vals = {str(t.get("department")) for t in self.trials}
            opts = sorted(v for v in vals if v and v != "0")
            return ["All"] + opts if opts else ["All"]
        return ["All"]

    # ---------- Derived: filtered trials ----------
    @rx.var
    def filtered_trials(self) -> List[Dict]:
        """Filter trials based on current filter settings"""
        data = list(self.trials)
        
        # Search filter
        q = self.query.lower().strip()
        if q:
            data = [t for t in data if 
                    q in str(t.get("title", "")).lower() or 
                    q in str(t.get("protocol_id", "")).lower()]
        
        # Status filter
        if self.status != "All":
            data = [t for t in data if str(t.get("status", "")) == self.status]
        
        # Phase filter
        if self.phase != "All":
            data = [t for t in data if str(t.get("phase", "")) == self.phase]
        
        # Priority filter
        if self.priority != "All":
            data = [t for t in data if str(t.get("priority", "")) == self.priority]
        
        # Therapeutic area filter
        if self.therapeutic_area != "All":
            data = [t for t in data if str(t.get("therapeutic_area", "")) == self.therapeutic_area]
        
        # Department filter (if applicable)
        if self.department != "All" and data and "department" in data[0]:
            data = [t for t in data if str(t.get("department", "")) == self.department]
        
        return data

    # ---------- Selection helpers ----------
    @rx.var
    def selected_trial(self) -> Dict | None:
        """Current selected trial (falls back to first filtered trial) or None if nothing selected (default)"""
        if not self.selected_trial_id:
            return None
        target = str(self.selected_trial_id)

        for t in self.filtered_trials:
            if str(t.get("id", "")) == target or str(t.get("protocol_id", "")) == target:
                return t
        return None
    
    @rx.var
    def filtered_trials_with_counts(self) -> list[dict]:
        by_pid: dict[str, set[str]] = {}
        for a in self.allocations:
            pid = str(a.get("trial_id", "")).strip()
            rid = str(a.get("resource_id", "")).strip()
            if pid and rid:
                by_pid.setdefault(pid, set()).add(rid)

        # Attach resource_count to each filtered trial (by protocol_id)
        out: list[dict] = []
        for t in self.filtered_trials:
            pid = str(t.get("protocol_id", "")).strip()
            cnt = len(by_pid.get(pid, set()))
            out.append({**t, "resource_count": cnt})
        return out

    # ---------- KPI atoms (scalars only; no nested dicts) ----------
    # TODO - Update these to be reactive using data
    @rx.var
    def active_trials(self) -> int:
        return sum(1 for t in self.filtered_trials if str(t.get("status","")).lower() != "completed")

    @rx.var
    def planning_trials(self) -> int:
        return sum(1 for t in self.filtered_trials if str(t.get("status","")).lower() == "planning")

    @rx.var
    def planning_text(self) -> str:
        return f"{self.planning_trials} in planning"

    @rx.var
    def total_resources(self) -> int:
        return len(self.resources)

    @rx.var
    def fte_share(self) -> int:
        fte_cnt = sum(1 for r in self.resources if str(r.get("type")).upper() == "FTE")
        fsp_cnt = sum(1 for r in self.resources if str(r.get("type")).upper() in {"FSP","CONTRACTOR"})
        denom = max(1, fte_cnt + fsp_cnt)
        return round(100 * fte_cnt / denom)

    @rx.var
    def fsp_share(self) -> int:
        fte_cnt = sum(1 for r in self.resources if str(r.get("type")).upper() == "FTE")
        fsp_cnt = sum(1 for r in self.resources if str(r.get("type")).upper() in {"FSP","CONTRACTOR"})
        denom = max(1, fte_cnt + fsp_cnt)
        return round(100 * fsp_cnt / denom)

    @rx.var
    def total_resources_sub(self) -> str:
        return f"{self.fte_share}% FTE, {self.fsp_share}% FSP"

    @rx.var
    def avg_util(self) -> int:
        vals = [float(r.get("utilization") or 0) for r in self.resources]
        return round(sum(vals) / max(1, len(vals)))

    @rx.var
    def avg_util_value(self) -> str:
        return f"{self.avg_util}%"

    @rx.var
    def avg_util_sub(self) -> str:
        return (
            "Underutilized" if self.avg_util < 30
            else "Balanced workload" if self.avg_util <= 70
            else "High load"
        )

    # ---------- Trial Resource Summary (selected trial in Portfolio) ---------
    @rx.var
    def selected_protocol(self) -> str: 
        return self.selected_trial.get("protocol_id") if self.selected_trial else ""
    
    @rx.var
    def selected_phase(self) -> str:
        return self.selected_trial.get("phase") if self.selected_trial else ""
    
    @rx.var
    def selected_area(self) -> str:
        return self.selected_trial.get("therapeutic_area") if self.selected_trial else ""
    
    @rx.var
    def selected_allocations(self) -> List[Dict]:
        """
        Allocations for the selected trial. Tries trial_id first then protocol_id
        """
        if not self.selected_trial:
            return []
        tid = str(self.selected_trial.get("id", ""))
        pid = str(self.selected_trial.get("protocol_id", ""))
        out: List[Dict] = []
        for a in self.allocations:
            a_tid = str(a.get("trial_id", ""))
            a_pid = str(a.get("protocol_id", ""))
            if (tid and a_tid == tid) or (pid and (a_pid == pid or a_tid == pid)):
                out.append(a)
        return out

    @rx.var
    def selected_resource_ids(self) -> List[str]:
        # TODO - update resource_id to use actual NTIDs and not names
        ids = []
        for a in self.selected_allocations:
            rid = a.get("resource_id")
            if rid is not None:
                ids.append(str(rid))
        return sorted(set(ids))

    @rx.var
    def selected_allocated_resources_count(self) -> int:
        return len(self.selected_resource_ids)

    # Resource utilization metrics

    @rx.var
    def selected_weekly_hours(self) -> int:
        allocs = self.selected_allocations
        if not allocs:
            return 0

        # 1) Direct weekly_hours if present
        if "weekly_hours" in (allocs[0].keys() if allocs else {}):
            total = sum(float(a.get("weekly_hours") or 0.0) for a in allocs)
            return int(round(total))

    @rx.var
    def _per_resource_util_list(self) -> List[float]:
        """Derived per-resource utilization % using ONLY present columns."""
        allocs = self.selected_allocations
        if not allocs:
            return []

        caps = {str(r.get("id")): float(r.get("capacity") or 0.0)
                for r in self.resources if "id" in r and "capacity" in r}
        base_util = {str(r.get("id")): float(r.get("utilization") or 0.0)
                     for r in self.resources if "id" in r and "utilization" in r}

        has_hours = any("weekly_hours" in a for a in allocs)
        has_pct   = any("allocation_percentage" in a for a in allocs)

        by_res: dict[str, dict[str, float]] = {}
        for a in allocs:
            rid = str(a.get("resource_id", ""))
            if rid not in by_res:
                by_res[rid] = {"hours": 0.0, "pct": 0.0}
            if "weekly_hours" in a:
                by_res[rid]["hours"] += float(a.get("weekly_hours") or 0.0)
            if "allocation_percentage" in a:
                by_res[rid]["pct"] += float(a.get("allocation_percentage") or 0.0)

        utils: List[float] = []
        for rid, agg in by_res.items():
            cap = caps.get(rid, 0.0)
            if has_hours and cap > 0:
                u = (agg["hours"] / cap) * 100.0
            elif has_pct:
                u = agg["pct"]                    # already a percent
            else:
                u = base_util.get(rid, 0.0)       # fallback to resource.utilization if present
            utils.append(max(0.0, u))
        return utils

    @rx.var
    def selected_avg_util(self) -> int:
        vals = self._per_resource_util_list
        return int(round(sum(vals) / len(vals))) if vals else 0

    @rx.var
    def selected_overallocated(self) -> int:
        return sum(1 for u in self._per_resource_util_list if u > 100.0)

    def selected_underutilized(self) -> int:
        return sum(1 for u in self._per_resource_util_list if u < 30.0)

    # ---------- Resource Type split for selected trial ------------
    @rx.var
    def selected_type_counts(self) -> dict:
        if not self.selected_resource_ids:
            return {"fte": 0, "fsp": 0}
        
        # build id -> type lookup from Resource.csv
        typ = {str(r.get("name")): str(r.get("type", "")).upper() for r in self.resources if "name" in r and "type" in r}
        fte = 0
        fsp = 0

        for rid in self.selected_resource_ids:
            t = typ.get(str(rid), "")
            if t == "FTE":
                fte += 1
            else:
                # Bucket ANY non-FTE as FSP/Contractor (e.g., "FSP", "CONTRACTOR", blanks)
                fsp += 1
        return {"fte": fte, "fsp": fsp}

    @rx.var
    def selected_fte_pct(self) -> int:
        c = self.selected_type_counts
        denom = c["fte"] + c["fsp"]
        return round(100 * c["fte"] / denom) if denom else 0

    @rx.var
    def selected_fsp_pct(self) -> int:
        c = self.selected_type_counts
        denom = c["fte"] + c["fsp"]
        return 100 - self.selected_fte_pct if denom else 0

    @rx.var
    def selected_type_pie_bg(self) -> str:
        """CSS conic-gradient for the donut (with a 1% white gap)."""
        if self.selected_allocated_resources_count == 0:
            return "conic-gradient(#E5E7EB 0 100%)"
        f = max(0, min(100, self.selected_fte_pct))
        g1 = f
        g2 = min(100, f + 1)  # 1% white gap
        return f"conic-gradient(#3B82F6 0 {g1}%, #FFFFFF {g1}% {g2}%, #10B981 {g2}% 100%)"        

    # ---------- Functional Area (Role) distribution for selected trial ----------
    @rx.var
    def selected_functional_breakdown(self) -> list[dict]:
        """
        Weighted hours by functional area (role) for the *selected* trial,
        using selected_resource_ids (not selected_allocations).

        Hours source, in order of preference:
          - Allocation.weekly_hours  (if present)
          - Allocation.allocation_percentage × Resource.capacity (if both present)
        Only uses columns that exist in your CSVs.
        """
        pid = self.selected_trial_id
        if not pid or not self.selected_resource_ids:
            return []

        # Fast membership check for the selected resources.
        selected_rids = {str(rid) for rid in self.selected_resource_ids}

        # Lookups from Resource.csv (only if columns exist).
        cap_lookup = {str(r.get("name")): float(r.get("capacity") or 0.0)
                      for r in self.resources if "id" in r and "capacity" in r}
        role_lookup = {str(r.get("name")): (str(r.get("role")) or "Unknown")
                       for r in self.resources if "id" in r and "role" in r}

        # Determine which allocation fields we actually have.
        has_hours = any("weekly_hours" in a for a in self.allocations)
        has_pct   = any("allocation_percentage" in a for a in self.allocations)

        # Aggregate hours per *selected* resource, for the *selected* protocol.
        hours_by_res: dict[str, float] = {}
        for a in self.allocations:
            if str(a.get("trial_id", "")) != str(pid):
                continue
            rid = str(a.get("resource_id", "")).strip()
            if rid not in selected_rids:
                continue

            val = 0.0
            if has_hours and "weekly_hours" in a:
                val = float(a.get("weekly_hours") or 0.0)
            elif has_pct and "allocation_percentage" in a and rid in cap_lookup:
                pct = float(a.get("allocation_percentage") or 0.0)
                val = (pct / 100.0) * cap_lookup.get(rid, 0.0)

            if val:
                hours_by_res[rid] = hours_by_res.get(rid, 0.0) + val

        if not hours_by_res:
            return []

        # Roll up hours by functional area (role).
        by_role: dict[str, float] = {}
        for rid, hrs in hours_by_res.items():
            role = role_lookup.get(rid, "Unknown")
            by_role[role] = by_role.get(role, 0.0) + hrs

        items = [{"label": k, "hours": v} for k, v in by_role.items()]
        items.sort(key=lambda x: x["hours"], reverse=True)
        return items
    
    @rx.var
    def selected_functional_breakdown_colored(self) -> list[dict]:
        """Breakdown + color + pct for legend (derived from selected_resource_ids)."""
        data = self.selected_functional_breakdown
        total = sum(d["hours"] for d in data) or 1.0
        palette = ["#10B981", "#3B82F6", "#E11D48", "#F59E0B", "#7C3AED", "#06B6D4", "#A3E635"]
        out = []
        for i, d in enumerate(data):
            pct = int(round(100.0 * d["hours"] / total))
            out.append({**d, "pct": pct, "color": palette[i % len(palette)]})
        return out

    @rx.var
    def selected_functional_pie_bg(self) -> str:
        """CSS conic-gradient for the functional-area pie."""
        data = self.selected_functional_breakdown_colored
        if not data:
            return "conic-gradient(#E5E7EB 0 100%)"
        total = sum(d["hours"] for d in data) or 1.0
        start = 0.0
        segments = []
        for d in data:
            share = (d["hours"] / total) * 100.0
            end = start + share
            segments.append(f"{d['color']} {start:.4f}% {end:.4f}%")
            start = end
        return f"conic-gradient({', '.join(segments)})"
    
    # ---------- Department (hours) for selected trial ----------
    @rx.var
    def selected_department_breakdown(self) -> list[dict]:
        """
        Returns: [{"label": department, "hours": float}, ...] for the *selected* trial.
        Hours source, in order of preference:
          - Allocation.weekly_hours
          - Allocation.allocation_percentage × Resource.capacity   (only if both exist)
        Uses only columns that actually exist.
        """
        pid = self.selected_trial_id
        if not pid or not self.selected_resource_ids:
            return []

        selected_rids = {str(rid) for rid in self.selected_resource_ids}

        # lookups from Resource.csv
        cap_lookup = {str(r.get("name")): float(r.get("capacity") or 0.0)
                      for r in self.resources if "id" in r and "capacity" in r}
        dept_lookup = {str(r.get("name")): (str(r.get("department")) or "Unknown")
                       for r in self.resources if "id" in r and "department" in r}

        # see what allocation fields we have
        has_hours = any("weekly_hours" in a for a in self.allocations)
        has_pct   = any("allocation_percentage" in a for a in self.allocations)

        # hours per selected resource, for the selected protocol
        hours_by_res: dict[str, float] = {}
        for a in self.allocations:
            if str(a.get("trial_id", "")) != str(pid):
                continue
            rid = str(a.get("resource_id", "")).strip()
            if rid not in selected_rids:
                continue

            val = 0.0
            if has_hours and "weekly_hours" in a:
                val = float(a.get("weekly_hours") or 0.0)
            elif has_pct and "allocation_percentage" in a and rid in cap_lookup:
                pct = float(a.get("allocation_percentage") or 0.0)
                val = (pct / 100.0) * cap_lookup.get(rid, 0.0)

            if val:
                hours_by_res[rid] = hours_by_res.get(rid, 0.0) + val

        if not hours_by_res:
            return []

        # roll up by department
        by_dept: dict[str, float] = {}
        for rid, hrs in hours_by_res.items():
            dept = dept_lookup.get(rid, "Unknown")
            by_dept[dept] = by_dept.get(dept, 0.0) + hrs

        items = [{"label": k, "hours": v} for k, v in by_dept.items()]
        items.sort(key=lambda x: x["hours"], reverse=True)
        return items

    # data for recharts 
    @rx.var
    def selected_department_chart_data(self) -> list[dict]:
        return [
            {"department": d["label"], 
             "hours": round(float(d["hours"]), 2)} for d in self.selected_department_breakdown
        ]

    @rx.var
    def selected_department_count(self) -> int:
        """How many departments have non-zero hours for the selected trial."""
        return len(self.selected_department_breakdown)
    
    @rx.var
    def has_selected_department_data(self) -> bool:
        return self.selected_department_count > 0
    
    # ---------- Trial Resource Toggle (Charts/Resource) ----------
    show_resources_table: bool = False
    
    def show_charts(self):
        self.show_resources_table = False

    def show_resources(self):
        self.show_resources_table = True

    @rx.var
    def selected_resources_detail(self) -> list[dict]:
        pid = self.selected_trial_id
        if not pid or not self.selected_resource_ids:
            return []
                
        selected_rids = {str(rid) for rid in self.selected_resource_ids}    

        # resource lookups (use only columns that exist)
        R = {str(r.get("name")): r for r in self.resources if "name" in r}
        caps  = {rid: float(r.get("capacity") or 0.0) for rid, r in R.items() if "capacity" in r}
        names = {rid: str(r.get("name") or "") for rid, r in R.items() if "name" in r}
        roles = {rid: str(r.get("role") or "") for rid, r in R.items() if "role" in r}
        types = {rid: str(r.get("type") or "") for rid, r in R.items() if "type" in r}
        depts = {rid: str(r.get("department") or "") for rid, r in R.items() if "department" in r}  

        has_hours = any("weekly_hours" in a for a in self.allocations)
        has_pct   = any("allocation_percentage" in a for a in self.allocations) 

        agg: dict[str, dict] = {}
        for a in self.allocations:
            if str(a.get("trial_id", "")) != str(pid):
                continue
            rid = str(a.get("resource_id", "")).strip()
            if rid not in selected_rids:
                continue    

            row = agg.setdefault(rid, {
                "name": rid,
                "name": names.get(rid, ""),
                "role": roles.get(rid, ""),
                "type": types.get(rid, ""),
                "department": depts.get(rid, ""),
                "capacity": caps.get(rid, 0.0),
                "weekly_hours": 0.0,
                "allocation_pct": 0.0,
                "start_date": None,
                "end_date": None,
            })  

            if has_hours and "weekly_hours" in a:
                row["weekly_hours"] += float(a.get("weekly_hours") or 0.0)
            if has_pct and "allocation_percentage" in a:
                row["allocation_pct"] += float(a.get("allocation_percentage") or 0.0)   

            s = str(a.get("start_date") or "").strip() or None
            e = str(a.get("end_date") or "").strip() or None
            # take min start / max end where present
            if s:
                row["start_date"] = min(filter(None, [row["start_date"], s])) if row["start_date"] else s
            if e:
                row["end_date"] = max(filter(None, [row["end_date"], e])) if row["end_date"] else e 

        rows: list[dict] = []
        for rid, row in agg.items():
            hours = row["weekly_hours"]
            if hours == 0.0 and row["allocation_pct"] and row["capacity"]:
                hours = (row["allocation_pct"] / 100.0) * float(row["capacity"])    

            pct = row["allocation_pct"]
            if (pct == 0.0) and hours and row["capacity"]:
                pct = (hours / float(row["capacity"])) * 100.0  

            rows.append({
                **row,
                "weekly_hours": round(hours or 0.0, 1),
                "allocation_pct": int(round(pct or 0.0)),
                "date_range": f"{row['start_date']} - {row['end_date']}" if (row["start_date"] or row["end_date"]) else "",
            })  

        # sort highest allocation first
        rows.sort(key=lambda x: x["allocation_pct"], reverse=True)
        return rows 

    @rx.var
    def selected_resources_count(self) -> int:
        return len(self.selected_resources_detail)

    # ======================================== #
    # ---------- Resource States ------------- #
    # ======================================== #

    # UI States
    resources_search: str = ""
    resources_tab: str = "resources"   # resources | open_positions | capacity_planning | incoming

    # Tab counts (wire to real data later; resources tab already uses total_resources)
    open_positions_count: int = 9
    incoming_count: int = 0

    def set_resources_search(self, value: str): self.resources_search = value

    def set_resources_tab(self, value: str): self.resources_tab = value

    def _norm_name(s: str) -> str:
        s = (s or "").strip().lower()
        s = re.sub(r"^(dr|mr|mrs|ms|miss|prof)\.?\s+", "", s)   # drop titles
        s = re.sub(r"[^a-z\s]", "", s)                         # rm punct
        s = re.sub(r"\s+", " ", s)
        return s

    def _norm_col(s: str) -> str:
        # "Resource ID" == "resource_id" == "resource-id" == "resourceid"
        return re.sub(r"[^a-z0-9]", "", (s or "").lower())

    def _first(d: dict, keys: list[str]) -> str:
        """Return the first non-null field in d whose (normalized) name matches any of keys."""
        if not isinstance(d, dict):
            return ""
        want = {_norm_col(k) for k in keys}
        for dk, v in d.items():
            if _norm_col(dk) in want:
                return "" if v is None else str(v).strip()
        return ""

    @rx.var
    def filtered_resources(self) -> list[dict]:
        """Apply the search box to name/role/type/department (case-insensitive)."""
        q = (self.resources_search or "").strip().lower()
        base = self.normalized_resources
        
        if not q:
            return base

        def hits(row: dict) -> bool:
            return (
                q in row["name"].lower()
                or q in row["role"].lower()
                or q in row["type"].lower()
                or q in row["department"].lower()
            )

        return [r for r in base if hits(r)]

    @rx.var
    def total_resources(self) -> int:
        return len(self.filtered_resources)

    # ---------- Actions / Allocations panel state -----------
    allocations_data: list[dict] = []
    allocations_open: bool = False
    selected_resource_name: str = ""
    resource_allocations: dict[str, list[dict]] = {}

    def load_allocations_from_csv(self, path: str = "data/Allocation.csv"):
        """One-time load of allocations into state"""
        if self.allocations_data: # already loaded
            return
        import csv, pathlib
        p = pathlib.Path(path)
        if not p.exists():
            return
        with p.open("r", encoding="utf-8-sig", newline="") as f:
            self.allocations_data = list(csv.DictReader(f))

    # Convenience zero-arg wrapper for on_load (since on_load passes no args)
    def load_allocations(self):
        self.load_allocations_from_csv()

    def open_allocations(self, name: str):
        self.allocations_open = True
        self.selected_resource_name = name or ""
    
    def close_allocations(self):
        self.allocations_open = False
        self.selected_resource_name = ""
    
    def noop(self):  # placeholder for the other two buttons
        pass
    
    @rx.var
    def normalized_resources(self) -> list[dict]:
        base = self.resources or []
        out: list[dict] = []
        for r in base:
            name = (r.get("Name") or r.get("name") or "").strip()
            role = (r.get("Role") or r.get("role") or "").strip()
            dept = (r.get("Department") or r.get("department") or "").strip()
            tlab, tcolor, tbg = _type_style(r.get("Type") or r.get("type") or "")

            # Prefer an ID if your resources dataset has it; else use normalized name (TO ADD LATER)
            rid = _first(r, ["NTID", "Network ID", "Employee ID", "resource_ntid", "resource_guid"])
            join_key = (rid or _norm_name(name)).lower()

            out.append({
                "name": name,
                "role": role,
                "type": tlab,
                "type_color": tcolor,
                "type_bg": tbg,
                "department": dept,
                "join_key": join_key,
            })
        return out

    @rx.var
    def _allocations_grouped(self) -> dict[str, list[dict]]:
        """Group allocations by join_key (prefer ID, else normalized name)"""
        groups: dict[str, list[dict]] = {}
        rows = self.allocations_data or [] # populate from csv
        for a in rows:
            # Build the same join key as resources: prefer ID, else normalized person name
            rid    = _first(a, ["NTID", "Network ID", "Employee ID", "resource_ntid", "resource_guid"])
            person = _first(a, ["resource_id", "Resource", "Name", "Employee", "Assignee", "resource_name"])
            key    = (rid or _norm_name(person)).lower()
    
            # Normalize the fields we display (map snake_case columns too)
            trial  = _first(a, ["Trial", "Study", "Study Name", "Study Title", "trial_id"]) or "Unknown Trial"
            phase  = _first(a, ["Phase"])  # blank if your CSV doesn’t have it
            alloc  = _first(a, ["Allocation", "Percent", "FTE%", "Pct", "allocation_percentage"])

            if alloc and not str(alloc).endswith("%"):
                alloc = f"{alloc}%"
                wh = _first(a, ["Weekly Hours", "Hours", "WeeklyHours", "weekly_hours"])

            if wh and not str(wh).endswith("h"):
                wh = f"{wh}h"
                start = _first(a, ["Start Date", "Start", "From", "Begin", "start_date"])
                end = _first(a, ["End Date", "End", "To", "Finish", "end_date"])
    
            row = {"trial": trial, "phase": phase, "allocation": alloc,
                   "weekly_hours": wh, "start_date": start, "end_date": end}
            
            groups.setdefault(key, []).append(row)
        return groups

    @rx.var
    def selected_resource(self) -> dict:
        """Safe dict with the fields we display in the header of the panel"""
        for r in self.normalized_resources:
            if r["name"] == self.selected_resource_name:
                return r
        # fallback with a synthetic join_key
        return {"name": self.selected_resource_name, 
                "role": "", 
                "department": "",
                "type": "",
                "join_key": _norm_name(self.selected_resource_name)}

    @rx.var
    def selected_resource_allocations(self) -> list[dict]:
        key = self.selected_resource.get("join_key") or _norm_name(self.selected_resource_name)
        return self._allocations_grouped.get(key, [])

    @rx.var
    def has_selected_allocations(self) -> bool:
        return len(self.selected_resource_allocations) > 0

    # ---------- Footer ----------
    user_initials: str = "RA"
    user_name: str = "Rafael Abbariao"
    user_role: str = "Clinical Operations"

    def refresh(self):
        pass
