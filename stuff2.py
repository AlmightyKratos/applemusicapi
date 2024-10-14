from xml.etree import ElementTree
from itertools import batched
import polars as pl


def get_all_songs_df(bytes: bytes | str) -> pl.DataFrame:
    top_data = ElementTree.fromstring(bytes)

    root = top_data.find("dict")
    if root is None:
        raise Exception("nope1")

    songs = root.find("dict")
    if songs is None:
        raise Exception("nope2")

    song_data = songs.findall("dict")
    song_things = [
        {(t1.text or "none"): t2.text for t1, t2 in batched(song, 2) if t2.text}
        for song in song_data
    ]

    return pl.from_dicts(song_things).with_columns(
        pl.col("Play Count").cast(pl.Int64).fill_null(pl.lit(0)),
        pl.col("Total Time").cast(pl.Int64),
    )


def get_duplicate_songs(all_songs_df: pl.DataFrame) -> pl.DataFrame:
    return (
        all_songs_df.group_by(pl.col("Name", "Artist"))
        .agg(pl.len())
        .filter(pl.col("len") > 1)  # type: ignore
        .sort(pl.col("Artist"), nulls_last=True)
    )


def get_most_listened_artists(df: pl.DataFrame):
    return (
        df.group_by(pl.col("Artist")).agg(pl.len()).sort(pl.col("len"), descending=True)
    )


def get_most_time_listened_to_artists(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.group_by(pl.col("Artist"))
        .agg((pl.col("Total Time") * pl.col("Play Count")).sum().alias("Stuff"))
        .sort(pl.col("Stuff"), descending=True)
    )


def get_most_time_listened_to_songs(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.with_columns(
            (pl.col("Total Time") * pl.col("Play Count")).alias("Total Song Time")
        )
        .sort(pl.col("Total Song Time"), descending=True)
        .select(["Total Song Time", "Artist", "Name"])
    )


def get_most_plays_per_track_artists(df: pl.DataFrame) -> pl.DataFrame:
    df_most_listened = (
        df.group_by(pl.col("Artist"))
        .agg(
            [
                pl.sum("Play Count"),
                pl.len().alias("Song Count"),
                (pl.sum("Play Count") / pl.len()).alias("Plays per Song"),
            ]
        )
        .sort(pl.col("Plays per Song"), descending=True)
    )
    return df_most_listened


def get_all_songs_df2(bytes: bytes | str) -> pl.DataFrame:
    top_data = ElementTree.fromstring(bytes)

    song_data = top_data.findall("dict")
    song_things = [
        {(t1.text or "none"): t2.text for t1, t2 in batched(song, 2) if t2.text}
        for song in song_data
    ]

    return pl.from_dicts(song_things).with_columns(
        pl.col("Play Count").cast(pl.Int64).fill_null(pl.lit(0)),
        pl.col("Total Time").cast(pl.Int64),
    )
