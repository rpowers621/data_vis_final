from jupyter_dash import JupyterDash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


import pandas as pd

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("blockbuster-top_ten_movies_per_year_DFE.csv")

available_indicators = ["Genre_1", "Genre_2", "Genre_3", "rating", "studio"]

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="xaxis-column",
                            options=[
                                {"label": i, "value": i} for i in available_indicators
                            ],
                            value="studio",
                        ),
                    ],
                    style={"width": "48%", "display": "inline-block"},
                ),
            ]
        ),
        dcc.Graph(id="indicator-graphic"),
        dcc.Slider(
            id="year--slider",
            min=df["year"].min(),
            max=df["year"].max(),
            value=df["year"].max(),
            marks={
                1975: "1975",
                1980: "1980",
                1985: "1985",
                1990: "1990",
                1995: "1995",
                2000: "2000",
                2005: "2005",
                2010: "2010",
                2014: "2014",
            },
            step=None,
        ),
    ]
)


@app.callback(
    Output("indicator-graphic", "figure"),
    Input("xaxis-column", "value"),
    Input("year--slider", "value"),
)
def update_graph(xaxis_column_name, year_value):
    dff = df[df["year"] == year_value]
    df2 = dff.groupby(xaxis_column_name).size().reset_index(name="count")
    fig = px.bar(
        x=df2[xaxis_column_name],
        y=df2["count"],
    )
    fig.update_layout(margin={"l": 40, "b": 40, "t": 10, "r": 0}, hovermode="closest")
    fig.update_xaxes(title=xaxis_column_name)
    fig.update_yaxes(title="Count")

    return fig


if __name__ == "__main__":
    app.run_server(mode="inline")
