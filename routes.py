import os
import pandas as pd
import plotly_express as px
import flask
import chart_studio.plotly as py
import chart_studio
import random
from flask import current_app as app


username = "rpowers621"
api_key = "mhJ0j9j2U7IdVkCzmpVp"

chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

blockbuster = pd.read_csv("blockbuster-top_ten_movies_per_year_DFE.csv")


def get_decade(start, end):
    decade_df = blockbuster[blockbuster["year"] <= end]
    decade_df = decade_df[decade_df["year"] >= start]

    return decade_df.reset_index(drop=True)


def make_genre_graph(column, data, i):
    fig = px.bar(data, x=column, y="count", title=f"Top Movie Genre: Genre {i}")
    fig.write_image(f"static/genre{i}.jpeg")


def make_rating_graph(data):
    ratings = data.groupby("rating").size().reset_index(name="count")
    fig = px.line(ratings, x="rating", y="count")
    py.plot(fig, filename="Top Movie By Rating", auto_open=False)

    count_max = ratings["count"].max()
    rating = ratings[ratings["count"] == count_max].astype("string")
    temp = rating["rating"].astype("string").tolist()

    return temp


def make_studio_graph(data):
    studio = data.groupby("studio").size().reset_index(name="count")
    fig = px.bar(studio, x="count", y="studio")
    py.plot(fig, filename="Top Movie By Studio", auto_open=False)

    count_max = studio["count"].max()
    studio2 = studio[studio["count"] == count_max].astype("string")
    temp = studio2["studio"].astype("string").tolist()
    return temp


def get_genre_stats(d_df):
    genre_list = ["Genre_1", "Genre_2", "Genre_3"]
    most_popular = []
    index = 1
    for i in genre_list:
        genres = (
            d_df.groupby(i).size().reset_index(name="count")
        )  # use this data for a graph

        make_genre_graph(i, genres, index)
        count_max = genres["count"].max()
        genre = genres[genres["count"] == count_max].astype("string")
        temp = genre[i].astype("string").tolist()
        most_popular.append(temp[0])
        temp = []
        index += 1

    return most_popular


@app.route("/")
def main():
    return flask.render_template("index.html")


@app.route("/results", methods=["POST"])
def results():

    decade = flask.request.form.get("decade")
    if decade:
        if decade == "75-84":
            start = 1975
            end = 1984
        elif decade == "85-94":
            start = 1985
            end = 1994
        elif decade == "95-04":
            start = 1995
            end = 2004
        elif decade == "05-14":
            start = 2005
            end = 2014
        df = get_decade(start, end)
        g_stats = get_genre_stats(df)
        rating = make_rating_graph(df)
        studio = make_studio_graph(df)

    return flask.render_template(
        "movie_breakdown.html",
        titles=df["title"],
        genre=df["Genre_1"],
        length=len(df),
        genre_1=g_stats[0],
        genre_2=g_stats[1],
        genre_3=g_stats[2],
        start=start,
        end=end,
        rating=rating[0],
        studio=studio[0],
        image_1="/static/genre1.jpeg",
        image_2="/static/genre2.jpeg",
        image_3="/static/genre3.jpeg",
    )


@app.route("/createblock", methods=["POST"])
def create_block():
    return flask.render_template("createblock.html")


def make_personal_stats(data, column, selection):
    df2 = data.groupby(column).size().reset_index(name="count")
    fig = px.pie(df2, values="count", names=column)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.write_image(f"static/{column}.jpeg")
    py.plot(fig, filename=f"Top Movie By {column}", auto_open=False)

    count_sum = df2["count"].sum()

    if selection in set(df2[column]):
        df3 = df2[df2[column] == selection].astype("string")
        count = df3["count"].astype("int").tolist()
        return int((count[0] / count_sum) * 100)
    else:
        return 0


def get_similar(dataframe, genre, studio):
    df = dataframe[dataframe["studio"] == studio]
    df2 = df[df["Genre_1"] == genre]
    print(df2["title"])
    titles = df2["title"].astype("string").tolist()
    imgs = df2["poster_url"].astype("string").tolist()
    title, img = None, None
    if titles:
        title = random.choice(titles)
    if imgs:
        img = random.choice(imgs)
    return title, img


@app.route("/movie_info", methods=["POST"])
def movie_info():

    decade = flask.request.form.get("decade")
    if decade:
        if decade == "75-84":
            start = 1975
            end = 1984
        elif decade == "85-94":
            start = 1985
            end = 1994
        elif decade == "95-04":
            start = 1995
            end = 2004
        elif decade == "05-14":
            start = 2005
            end = 2014
        df = get_decade(start, end)
        g1 = flask.request.form.get("genre_1")  # 70%
        per_g1 = make_personal_stats(df, "Genre_1", g1)

        g2 = flask.request.form.get("genre_2")  # 20%
        per_g2 = make_personal_stats(df, "Genre_2", g2)

        g3 = flask.request.form.get("genre_3")  # 10%
        per_g3 = make_personal_stats(df, "Genre_3", g3)

        rating = flask.request.form.get("rating")
        per_rating = make_personal_stats(df, "rating", rating)

        studio = flask.request.form.get("studio")
        per_studio = make_personal_stats(df, "studio", studio)

        title, img = get_similar(df, g1, studio)

    return flask.render_template(
        "createblock.html",
        start=start,
        end=end,
        g1=per_g1,
        g2=per_g2,
        g3=per_g3,
        rating=per_rating,
        studio=per_studio,
        title=title,
        img=img,
    )
