import reflex as rx
import plotly.graph_objects as go
from app.state import AppState as State

def donut(data: dict, title: str) -> rx.Component:
    labels = list(data.keys())
    values = list(data.values())
    fig = go.Figure(
        data=[go.Pie(labels=labels, values=values, hole=0.6, textinfo="none")]
    )
    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", y=-0.1),
        height=300,
    )
    return rx.plotly(fig)

def bar(data: dict, title: str) -> rx.Component:
    labels = list(data.keys())
    values = list(data.values())
    fig = go.Figure(
        data=[go.Bar(x=labels, y=values)]
    )
    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=40, b=10),
        height=320,
    )
    return rx.plotly(fig)

def resource_type_donut() -> rx.Component:
    return rx.cond(
        State.has_selection,
        rx.box(),  # nothing until selected
        donut(State.sel_alloc["resource_type"], "Resource Type Distribution"),
    )

def functional_area_donut() -> rx.Component:
    return rx.cond(
        State.has_selection,
        rx.box(),
        donut(State.sel_alloc["functional_area"], "Functional Area Distribution"),
    )

def hours_by_dept_bar() -> rx.Component:
    return rx.cond(
        State.has_selection,
        rx.box(),
        bar(State.sel_alloc["hours_by_dept"], "Hours by Department"),
    )
