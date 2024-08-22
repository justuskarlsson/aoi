import json
import os
from pathlib import Path
from dataclasses import dataclass

__all__ = ["Feature", "MultiPolygon", "load", "select_biggest"]

data_dir = Path(__file__).parent.parent / "data"


@dataclass
class MultiPolygon:
    coordinates: list[list[list[list[float]]]]

@dataclass
class Polygon:
    coordinates: list[list[list[float]]]

@dataclass
class Feature:
    properties: dict[str, any]
    geometry: MultiPolygon | Polygon
        

def load(name: str):
    path = data_dir / (name + ".geojson")
    if not os.path.exists(path):
        raise Exception(f"{path} does not exist")
    with open(path) as f:
        geojson = json.load(f)
    aoi = Feature(
        geojson["properties"],
        geometry=MultiPolygon(geojson["geometry"]["coordinates"])
    )
    return aoi

def select_biggest(feat: Feature):
    sizes = []
    geom = feat.geometry.coordinates
    for poly in geom:
        sizes.append(
            (len(poly[0]), len(sizes),)
        )
    sizes.sort(reverse=True)
    _, biggest_idx = sizes[0]
    return Feature(
        feat.properties,
        Polygon(geom[biggest_idx])
    )


