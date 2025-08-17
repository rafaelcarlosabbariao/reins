import reflex as rx
from datetime import date
from typing import Optional

class AppState(rx.State):
    # Sidebar resource ratios 
    fte_pct: int = 60
    fsp_pct: int = 40

    kpis = {
        "Flex Ratio": "—",
        "Utilization": "—",
        "Late-Phase %": "—",
        "Headcount Gap": "—",
    }

    # Return a JSON-seriazable dict of the state
    @rx.var
    def kpi_pairs(self) -> list[list[str]]:
        return [[k, v] for k, v in self.kpis.items()]

    # ====== Home Page Data ===== #

    # Pipeline data
    pipeline_snapshot_asof: str = date.today().strftime("%B %d, %Y")
    phase_counts: list[dict] = [
        {"label": "Phase 1", "phase": "P1", "value":9},
        {"label": "Phase 2", "phase": "P2", "value":8},
        {"label": "Phase 3", "phase": "P3", "value":7},
        {"label": "Registration", "phase": "REG", "value":2}
    ]

    @rx.var
    def phase_total(self) -> int:
        return sum(int(x.get("value", 0)) for x in self.phase_counts)
    
    # Areas of Focus
    therapeutic_areas: list[dict] = [
        {
            "title":"Internal Medicine",
            "count": 6,
            "img":"/ta/internal_medicine.png",
            "href":"/portfolio?ta=IM",
        },
        {
            "title": "Inflammation & Immunology",
            "count": 5,
            "img": "/ta/inflammation_and_immunology.png",
            "href": "/portfolio?ta=I&I",
        },
        {
            "title": "Vaccines",
            "count": 6,
            "img": "/ta/vaccines.png",
            "href": "/portfolio?ta=Vaccines",
        },
        {
            "title": "Oncology",
            "count": 7,
            "img": "/ta/oncology.png",
            "href": "/portfolio?ta=Oncology",
        },
    ]

    # ===== Portfolio Data ===== #

    # Portfolio Data (use random static data for now)
    portfolio_active_trials: int = 15
    portfolio_in_planning: int = 7
    portfolio_total_resources: int = 18
    portfolio_fte_share: int = 67
    portfolio_fsp_share: int = 33
    portfolio_avg_util: int = 0

    # Filters (plain lists so foreach works)
    filter_status: list[str] = ["All Status", "Ongoing", "Planning", "Paused"]
    filter_phase: list[str]  = ["All Phases", "Phase I", "Phase II", "Phase III", "Registration"]
    filter_priority: list[str] = ["All Priority", "High", "Medium", "Low"]
    filter_area: list[str] = ["All Areas", "Internal Medicine", "Oncology", "Inflammation & Immunology", "Vaccines"]
    filter_dept: list[str] = ["All Departments", "Clinical Ops", "Biostats", "Data Mgmt", "Supply"]

    selected_status: str = "All Status"
    selected_phase: str = "All Phases"
    selected_priority: str = "All Priority"
    selected_area: str = "All Areas"
    selected_dept: str = "All Departments"

    # Trial list (stub; replace with your real data)
    trials: list[dict] = [
        {
            "id": "NPS-IM-001",
            "title": "Non-Project Specific Activities - Internal Medicine",
            "status": "Ongoing",
            "phase": "Phase I",
            "area": "Internal Medicine",
        },
        {
            "id": "NPS-ONC-001",
            "title": "Non-Project Specific Activities - Oncology",
            "status": "Ongoing",
            "phase": "Phase I",
            "area": "Oncology",
        },
        {
            "id": "NPS-II-001",
            "title": "Non-Project Specific Activities - Inflammation & Immunology",
            "status": "Ongoing",
            "phase": "Phase I",
            "area": "Inflammation & Immunology",
        },
        {
            "id": "ONC-001",
            "title": "Prostate Cancer Immunotherapy",
            "status": "Ongoing",
            "phase": "Phase II",
            "area": "Oncology",
            "priority": "High",
        },
        {
            "id": "IM-203",
            "title": "Hypertension Management Study",
            "status": "Ongoing",
            "phase": "Registration",
            "area": "Internal Medicine",
            "priority": "Medium",
        },
        {
            "id": "II-401",
            "title": "Rheumatoid Arthritis Biologic Therapy",
            "status": "Planning",
            "phase": "Phase II",
            "area": "Inflammation & Immunology",
            "priority": "High",
        },
    ]

    selected_trial_id: Optional[str] = None

    def select_trial(self, trial_id: str):
        self.selected_trial_id = trial_id

    @rx.var
    def selected_trial(self) -> dict | None:
        for t in self.trials:
            if t["id"] == self.selected_trial_id:
                return t
        return None

    @rx.var
    def has_selection(self) -> bool:
        return self.selected_trial is not None
    
    @rx.var
    def sel_weekly_hours_label(self) -> str:
        alloc = self.sel_alloc
        if not alloc:
            return "0h"
        return f"{alloc['weekly_hours']}h"
    
    @rx.var
    def sel_avg_util_label(self) -> str:
        alloc = self.sel_alloc
        if not alloc:
            return "0%"
        return f"{alloc['avg_util']}%"

    @rx.var
    def sel_over_alloc_label(self) -> str:
        alloc = self.sel_alloc
        if not alloc:
            return "0%"
        return f"{alloc['over_allocated']}%"
    
    @rx.var
    def sel_sites_counts_label(self) -> str:
        alloc = self.sel_alloc
        if not alloc:
            return "0 sites"
        return f"{len(alloc['sites'])} sites"

    # ===== Allocations for the allocated trial (mock) =====
    # keyed by trial_id
    allocations: dict = {
        "ONC-001": {
            "allocated_resources": 2,
            "weekly_hours": 20,         # total hours/week
            "avg_util": 26,             # %
            "over_allocated": 0,        # %
            "resource_type": {          # donut
                "FTE": 51,
                "FSP": 49,
            },
            "functional_area": {        # donut
                "Clinical Ops": 60,
                "Biostatistics": 25,
                "Data Mgmt": 15,
            },
            "hours_by_dept": {          # bar
                "Clinical Operations": 15,
                "Biostatistics (A&R)": 6,
            },
            "resources": [              # list
                {
                    "name": "Lisa Park",
                    "role": "Clinical Trial Manager",
                    "type": "FTE",
                    "dept": "Clinical Operations",
                    "util": 35,        # %
                    "hours_week": 14,
                    "range": "Jan 14 – Jun 29, 2025",
                },
                {
                    "name": "Chloe Sterling",
                    "role": "Recruitment Strategy Lead",
                    "type": "FTE",
                    "dept": "Optimization, Analytics & Recruitment Solutions (OARS)",
                    "util": 16,
                    "hours_week": 6,
                    "range": "Jan 14 – Jun 29, 2025",
                },
            ],
            "sites": [                  # simple mock site markers
                {"lat": 51.5074, "lon": -0.1278, "label": "London, UK"},
                {"lat": 48.8566, "lon": 2.3522, "label": "Paris, FR"},
                {"lat": 40.7128, "lon": -74.0060, "label": "New York, US"},
            ],
        }
    }

    @rx.var
    def sel_alloc(self) -> dict | None:
        t = self.selected_trial
        if t is None:
            return None
        return self.allocations.get(t["id"])

    # ===== Footer Card ===== #
    # Footer user card 
    user_initials: str = "RA"
    user_name: str = "Rafael Abbariao"
    user_role: str = "Clinical Operations"

    def refresh(self):
        # TODO: fetch live counts and TA totals; update resource ratio, phase_counts and areas_of_focus
        pass