import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[
            "/static/styles.css",
        ],
    )
    global DF
    DF = pd.read_csv("blockbuster-top_ten_movies_per_year_DFE.csv")

    available_indicators = ["Genre_1", "Genre_2", "Genre_3", "rating", "studio"]

    dash_app.layout = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Dropdown(
                                id="xaxis-column",
                                options=[
                                    {"label": i, "value": i}
                                    for i in available_indicators
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
                min=DF["year"].min(),
                max=DF["year"].max(),
                value=DF["year"].max(),
                marks={
                    1975: "1975",
                    1976: "1976",
                    1977: "1977",
                    1978: "1978",
                    1979: "1979",
                    1980: "1980",
                    1981: "1981",
                    1982: "1982",
                    1983: "1983",
                    1984: "1984",
                    1985: "1985",
                    1986: "1986",
                    1987: "1987",
                    1988: "1988",
                    1989: "1989",
                    1990: "1990",
                    1991: "1991",
                    1992: "1992",
                    1993: "1993",
                    1994: "1994",
                    1995: "1995",
                    1996: "1996",
                    1997: "1997",
                    1998: "1998",
                    1999: "1999",
                    2000: "2000",
                    2001: "2001",
                    2002: "2002",
                    2003: "2003",
                    2004: "2004",
                    2005: "2005",
                    2006: "2006",
                    2007: "2007",
                    2008: "2008",
                    2009: "2009",
                    2010: "2010",
                    2011: "2011",
                    2012: "2012",
                    2013: "2013",
                    2014: "2014",
                },
                step=None,
            ),
        ]
    )
    init_callbacks(dash_app)
    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(
        Output("indicator-graphic", "figure"),
        Input("xaxis-column", "value"),
        Input("year--slider", "value"),
    )
    def update_graph(xaxis_column_name, year_value):
        dff = DF[DF["year"] == year_value]
        df2 = dff.groupby(xaxis_column_name).size().reset_index(name="count")
        fig = px.bar(
            x=df2[xaxis_column_name],
            y=df2["count"],
        )
        fig.update_layout(
            margin={"l": 40, "b": 40, "t": 10, "r": 0}, hovermode="closest"
        )
        fig.update_xaxes(title=xaxis_column_name)
        fig.update_yaxes(title="Count")

        return fig

    # Create Dash Layout
