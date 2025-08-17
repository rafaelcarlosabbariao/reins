import reflex as rx
from app.state import AppState as State

def resource_type_donut() -> rx.Component:
    return rx.cond(State.has_selection, rx.plotly(State.sel_resource_type_fig), rx.box())

def functional_area_donut() -> rx.Component:
    return rx.cond(State.has_selection, rx.plotly(State.sel_functional_area_fig), rx.box())

def hours_by_dept_bar() -> rx.Component:
    return rx.cond(State.has_selection, rx.plotly(State.sel_hours_by_dept_fig), rx.box())
