# app/state.py
from __future__ import annotations
import reflex as rx
from datetime import date
from pathlib import Path
from typing import Optional, List, Dict
import pandas as pd

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

    # ---------- Selection for Trials panel ----------
    selected_trial_id: str | None = None

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

        if not t.empty:
            keep_t = [
                "id", "title", "protocol_id", "phase", "therapeutic_area", "status",
                "start_date", "end_date", "fte_allocation", "fsp_allocation",
                "priority", "sites_count",
            ]
            self.trials = t[[c for c in keep_t if c in t.columns]].fillna(0).to_dict("records")
        else:
            self.trials = []

        if not r.empty:
            keep_r = ["id", "name", "type", "role", "utilization"]
            self.resources = r[[c for c in keep_r if c in r.columns]].fillna(0).to_dict("records")
        else:
            self.resources = []

        # No default trial selected 
        self.selected_trial_id = None

    # ---------- Actions / Event Handlers ----------
    # explicit setters (and aliases) - avoids set_* vs set_*_ collisions
    def set_query(self, value: str): self.query = value
    def set_query_(self, value: str): self.query = value

    def set_status(self, value: str): self.status = value
    def set_status_(self, value: str): self.status = value

    def set_phase(self, value: str): self.phase = value
    def set_phase_(self, value: str): self.phase = value

    def set_priority(self, value: str): self.priority = value
    def set_priority_(self, value: str): self.priority = value

    def set_therapeutic_area(self, value: str): self.therapeutic_area = value
    def set_therapeutic_area_(self, value: str): self.therapeutic_area = value

    def set_department(self, value: str): self.department = value
    def set_department_(self, value: str): self.department = value

    def select_trial(self, trial_id: str):
        self.selected_trial_id = trial_id

    def clear_selection(self):
        self.selected_trial_id = None

    # ---------- Options (reactive lists) ---------- 
    @rx.var
    def status_options(self) -> List[str]:
        vals = {str(t.get("status")) for t in self.trials if "status" in t}
        return ["All"] + sorted(v for v in vals if v and v != "0")
    
    @rx.var
    def phase_options(self) -> List[str]:
        vals = {str(t.get("phase")) for t in self.trials if "phase" in t}
        return ["All"] + sorted(v for v in vals if v and v != "0")
    
    @rx.var
    def priority_options(self) -> List[str]:
        vals = {str(t.get("priority")) for t in self.trials if "priority" in t}
        return ["All"] + sorted(v for v in vals if v and v != "0")
    
    @rx.var
    def area_options(self) -> List[str]:
        vals = {str(t.get("therapeutic_area")) for t in self.trials if "therapeutic_area" in t}
        return ["All"] + sorted(v for v in vals if v and v != "0")
    
    @rx.var
    def department_options(self) -> List[str]:
        # Only populate if the dataset has 'department'; otherwise return just All
        if self.trials and "department" in self.trials[0]:
            vals = {str(t.get("department")) for t in self.trials}
            opts = sorted(v for v in vals if v and v != "0")
            return ["All"] + opts if opts else ["All"]
        return ["All"]

    # ---------- Derived: filtered trials ----------
    @rx.var
    def filtered_trials(self) -> List[Dict]:
        data = list(self.trials)
        q = self.query.lower().strip()
        if q:
            data = [t for t in data if q in str(t.get("title","")).lower() or q in str(t.get("protocol_id","")).lower()]
        if self.phase != "All":
            data = [t for t in data if t.get("phase") == self.phase]
        if self.priority != "All":
            data = [t for t in data if t.get("priority") == self.priority]
        if self.therapeutic_area != "All":
            data = [t for t in data if t.get("therapeutic_area") == self.therapeutic_area]
        if self.status != "All":
            data = [t for t in data if t.get("status") == self.status]
        if self.department != "All" and (data and "department" in data[0]):
            data = [t for t in data if t.get("department") == self.department]
        return data

    # ---------- Selection helpers ----------
    @rx.var
    def selected_trial(self) -> Dict | None:
        """Current selected trial (falls back to first filtered trial) or None if nothing selected (default)"""
        if not self.selected_trial_id:
            return None
        return next((t for t in set.filtered_trials if t.get("id") == self.selected_trial_id), None)

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

    # ---------- Footer ----------
    user_initials: str = "RA"
    user_name: str = "Rafael Abbariao"
    user_role: str = "Clinical Operations"

    def refresh(self):
        pass
