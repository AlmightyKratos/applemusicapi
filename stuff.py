# Function to parse the XML and convert it to a list of dictionaries
import io
import pathlib
from typing import Any
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from pydantic import BaseModel, ConfigDict, Field


class Song(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    track_id: int = Field(alias="Track ID")
    name: str = Field(alias="Name")
    artist: str = Field(alias="Artist")
    album_artist: str = Field(alias="Album Artist")
    composer: str = Field(alias="Composer")
    album: str = Field(alias="Album")
    genre: str = Field(alias="Genre")
    kind: str = Field(alias="Kind")
    size: int = Field(alias="Size")
    total_time: int = Field(alias="Total Time")
    disc_number: int = Field(alias="Disc Number")
    disc_count: int = Field(alias="Disc Count")
    track_number: int = Field(alias="Track Number")
    track_count: int = Field(alias="Track Count")
    year: int = Field(alias="Year")
    date_modified: str = Field(alias="Date Modified")
    date_added: str = Field(alias="Date Added")
    bit_rate: int = Field(alias="Bit Rate")
    sample_rate: int = Field(alias="Sample Rate")
    play_count: int = Field(alias="Play Count")
    play_date: str = Field(alias="Play Date")
    play_date_utc: str = Field(alias="Play Date UTC")
    release_date: str = Field(alias="Release Date")
    artwork_count: int = Field(alias="Artwork Count")
    sort_album: str = Field(alias="Sort Album")
    sort_artist: str = Field(alias="Sort Artist")
    sort_name: str = Field(alias="Sort Name")
    persistent_id: str = Field(alias="Persistent ID")
    track_type: str = Field(alias="Track Type")
    apple_music: bool = Field(alias="Apple Music")


def parse_dict_element(element: Element) -> dict[Any, Any]:
    data_dict = {}
    it = iter(element)
    for key in it:
        if key.tag == "key":
            value = next(it)
            match value.tag:
                case "dict":
                    data_dict[key.text] = parse_dict_element(value)
                # case "true":
                #     data_dict[key.text] = True
                # case "false":
                #     data_dict[key.text] = False
                case "integer":
                    data_dict[key.text] = (
                        None if value.text is None else int(value.text)
                    )
                # case "date":
                #     data_dict[key.text] = value.text
                case _:
                    data_dict[key.text] = value.text
    # breakpoint()
    return data_dict


def parse_xml_to_dicts(xml_file: pathlib.Path | io.BytesIO) -> list[Song]:
    tree = ElementTree.parse(xml_file)
    root = tree.getroot().find("dict")

    if root is None or type(root) is not Element:
        return []

    plist_dict = parse_dict_element(root)
    tracks = plist_dict["Tracks"]

    # records = []
    # for _, track_info in tracks.items():
    #     records.append(track_info)

    return tracks


path = pathlib.Path("src/app/api/musics1/music_library.xml")
dicts = parse_xml_to_dicts(path)
print(dicts)
