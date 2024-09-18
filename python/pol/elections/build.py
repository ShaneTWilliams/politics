import datetime
import json
import re
import xml

import geopandas
import openpyxl
from pol.elections.structures import *
from pol.paths import (
    ARTIFACT_DIR,
    CACHE_DIR,
    PYTHON_PACKAGE_DIR,
    SOURCES_DIR,
    WEB_ARTIFACT_DIR,
)
from shapely.geometry import Polygon

PARTY_COLORS = {
    "Liberal Party of Canada": Color.RED,
    "Anti-Confederate": Color.ORANGE,
    "New Democratic Party": Color.ORANGE,
    "Conservative (1867-1942)": Color.BLUE,
    "Conservative Party of Canada": Color.BLUE,
    "Green Party of Canada": Color.GREEN,
    "Liberal-Conservative": Color.PURPLE,
    "Bloc Québécois": Color.YELLOW,
    "Independent": Color.GREY,
}

GEOMETRY_DIR = SOURCES_DIR / "geometry/fedshapes_cbf_20221003"
RO_YEARS = sorted([int(f.stem[6:10]) for f in GEOMETRY_DIR.glob("*.shp")])

DETAIL_MAP_BOUNDS = {
    DetailViewName.ST_JOHNS: {
        "x": 8900000,
        "y": 2200000,
        "width": 100000,
        "height": 100000,
    },
    DetailViewName.PEI: {"x": 8340000, "y": 1650000, "width": 50000, "height": 50000},
    DetailViewName.MONCTON: {
        "x": 8200000,
        "y": 1600000,
        "width": 100000,
        "height": 100000,
    },
    DetailViewName.HALIFAX: {
        "x": 8360000,
        "y": 1490000,
        "width": 100000,
        "height": 100000,
    },
    DetailViewName.MONTREAL: {
        "x": 7595000,
        "y": 1270000,
        "width": 50000,
        "height": 50000,
    },
    DetailViewName.QUEBEC_CITY: {
        "x": 7730000,
        "y": 1470000,
        "width": 50000,
        "height": 50000,
    },
    DetailViewName.SOUTHERN_QUEBEC: {
        "x": 7580000,
        "y": 1350000,
        "width": 200000,
        "height": 200000,
    },
    DetailViewName.TROIS_RIVIERES: {
        "x": 7650000,
        "y": 1380000,
        "width": 50000,
        "height": 50000,
    },
    DetailViewName.OTTAWA: {
        "x": 7430000,
        "y": 1220000,
        "width": 70000,
        "height": 70000,
    },
    DetailViewName.TORONTO: {
        "x": 7190000,
        "y": 960000,
        "width": 60000,
        "height": 60000,
    },
    DetailViewName.GOLDEN_HORSESHOE: {
        "x": 7100000,
        "y": 1030000,
        "width": 200000,
        "height": 200000,
    },
    DetailViewName.LONDON: {"x": 7060000, "y": 850000, "width": 50000, "height": 50000},
    DetailViewName.REGINA: {
        "x": 5280000,
        "y": 1700000,
        "width": 50000,
        "height": 50000,
    },
    DetailViewName.WINNIPEG: {
        "x": 5800000,
        "y": 1565000,
        "width": 50000,
        "height": 50000,
    },
    DetailViewName.ESSEX: {"x": 6930000, "y": 750000, "width": 50000, "height": 50000},
    DetailViewName.SASKATOON: {
        "x": 5180000,
        "y": 1910000,
        "width": 50000,
        "height": 50000,
    },
    DetailViewName.CALGARY: {
        "x": 4660000,
        "y": 1950000,
        "width": 60000,
        "height": 60000,
    },
    DetailViewName.EDMONTON: {
        "x": 4780000,
        "y": 2200000,
        "width": 70000,
        "height": 70000,
    },
    DetailViewName.VANCOUVER: {
        "x": 3990000,
        "y": 2030000,
        "width": 70000,
        "height": 70000,
    },
    DetailViewName.VICTORIA: {
        "x": 3920000,
        "y": 1970000,
        "width": 50000,
        "height": 50000,
    },
}

detail_map_polygons = {}
for city, bounds in DETAIL_MAP_BOUNDS.items():
    detail_map_polygons[city] = Polygon(
        [
            (bounds["x"], bounds["y"]),
            (bounds["x"] + bounds["width"], bounds["y"]),
            (bounds["x"] + bounds["width"], bounds["y"] - bounds["height"]),
            (bounds["x"], bounds["y"] - bounds["height"]),
        ]
    )


class Geometry:
    def __init__(self, name: str, id: int, shape: Polygon):
        self.name = name
        self.id = id
        self.shape = shape

    @property
    def area(self):
        return int(self.shape.area / 1e6)

    def intersects(self, other):
        return self.shape.intersects(other)

    @staticmethod
    def process_svg(svg):
        for attr_key in ["fill", "stroke", "stroke-width", "opacity"]:
            svg.attrib.pop(attr_key, None)

        if "d" not in svg.attrib:
            return

        new_d = []
        for split1 in svg.attrib["d"].split(" "):
            new_split1 = []
            for split2 in split1.split(","):
                try:
                    float(split2)
                except ValueError:
                    new_split1.append(split2)
                    continue
                new_split1.append(f"{float(split2):.0f}")
            new_d.append(",".join(new_split1))
        svg.attrib["d"] = " ".join(new_d)

    def to_svg(self, tolerance) -> str:
        simple_geometry = self.shape.simplify(tolerance, preserve_topology=False)
        svg = simple_geometry.svg()
        xml_svg = xml.etree.ElementTree.fromstring(svg)
        self.process_svg(xml_svg)
        for child in xml_svg:
            self.process_svg(child)

        return xml.etree.ElementTree.tostring(xml_svg).decode("utf-8")


def get_cached_xlsx(xlsx_path, json_path):
    if not json_path.exists():
        rows = []
        workbook = openpyxl.load_workbook(xlsx_path)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            rows.append(row)

        if not json_path.parent.exists():
            json_path.parent.mkdir(parents=True, exist_ok=True)

        with open(json_path, "w") as f:
            json.dump(rows, f, indent=4)

    with open(json_path) as f:
        return json.load(f)


def load_geo_ridings():
    ridings = {year: [] for year in RO_YEARS}

    for year in RO_YEARS:
        gdf = geopandas.read_file(
            SOURCES_DIR / f"geometry/fedshapes_cbf_20221003/CBF_RO{year}_CSRS.shp",
            engine="pyogrio",
        )

        for _, row in gdf.iterrows():
            if year in [1867, 1872]:
                _, _, name, id, _, notes, geometry = row.tolist()
            elif year in [1882]:
                _, _, name, id, notes, _, _, _, geometry = row.tolist()
            elif year in [1892, 1903, 1914, 1924, 1933, 1947, 1952, 1966, 1976]:
                _, _, name, id, _, geometry = row.tolist()
            elif year in [1905]:
                name, _, _, _, id, geometry = row.tolist()
            elif year in [1987]:
                _, id, _, _, name, geometry = row.tolist()
            elif year in [1996]:
                _, name, id, _, _, geometry = row.tolist()
            elif year in [1999]:
                _, name, _, id, _, geometry = row.tolist()
            elif year in [2003]:
                _, id, _, _, geometry = row.tolist()
                name = None
            elif year in [2013]:
                _, name, _, id, _, geometry = row.tolist()
            else:
                raise RuntimeError(f"Unhandled year: {year}")

            geometry_obj = Geometry(name, id, geometry)
            ridings[year].append(geometry_obj)
            if id == "186724041":
                ridings[1872].append(geometry_obj)
                ridings[1882].append(geometry_obj)

    return ridings


def build():
    ARTIFACT_DIR.mkdir(exist_ok=True)
    CACHE_DIR.mkdir(exist_ok=True)

    print("Loading geometry")
    geo_ridings = load_geo_ridings()
    #with open("geo_ridings.json", "w") as f:
    #    json.dump({year: [[r.name, r.id] for r in ridings] for year, ridings in geo_ridings.items()}, f)

    election_and_candidate_rows = get_cached_xlsx(
        SOURCES_DIR / "electionsCandidates.xlsx", CACHE_DIR / "electionsCandidates.json"
    )
    riding_rows = get_cached_xlsx(
        SOURCES_DIR / "ParlInfoRidings.xlsx", CACHE_DIR / f"ridings.json"
    )
    parliamentarians_rows = get_cached_xlsx(
        SOURCES_DIR / "Parliamentarians.xlsx", CACHE_DIR / f"parliamentarians.json"
    )

    with open(PYTHON_PACKAGE_DIR / "elections/corrections.json", "r") as f:
        corrections = json.load(f)

    data = {
        Parliament: [],
        Election: [],
        Party: set(),
        Riding: [],
        Candidate: [],
        Run: [],
        DetailView: [],
    }

    print("Processing ridings")
    riding_by_detail_view = {
        view_name: {year: [] for year in RO_YEARS}
        for view_name in DETAIL_MAP_BOUNDS.keys()
    }
    for row in riding_rows:
        name, province, region, start_date, end_date, status = row
        if start_date == "":
            start_date_obj = None
        else:
            start_year, start_month, start_day = start_date.split("-")
            start_date_obj = datetime.date(
                int(start_year), int(start_month), int(start_day)
            )

        # According to EC these ridings started on May 1st, 1871.
        # But these elections were held on March 2nd and 3rd, 1871!
        # https://en.wikipedia.org/wiki/Lisgar_(electoral_district)
        # https://en.wikipedia.org/wiki/Provencher
        if (name, start_date_obj) == ("Lisgar", datetime.date(1871, 5, 1)):
            start_date_obj = datetime.date(1871, 3, 2)
        elif (name, start_date_obj) == ("Marquette", datetime.date(1871, 5, 1)):
            start_date_obj = datetime.date(1871, 3, 2)
        elif (name, start_date_obj) == ("Selkirk", datetime.date(1871, 5, 1)):
            start_date_obj = datetime.date(1871, 3, 2)
        elif (name, start_date_obj) == ("Provencher", datetime.date(1871, 5, 1)):
            start_date_obj = datetime.date(1871, 3, 3)  # This one was a day late?

        if end_date == "":
            end_date_obj = None
        else:
            end_year, end_month, end_day = end_date.split("-")
            end_date_obj = datetime.date(int(end_year), int(end_month), int(end_day))

        if (
            start_date_obj.month == 1
            and start_date_obj.day == 1
            and end_date_obj.month == 1
            and end_date_obj.day == 1
        ):
            continue

        ro_years = []
        for year in RO_YEARS[::-1]:
            if end_date_obj is None or year <= end_date_obj.year:
                ro_years.append(year)
            if year <= start_date_obj.year:
                break

        geo_riding_by_year = {}
        for ro_year in ro_years:
            is_duplicate = len([r for r in geo_ridings[ro_year] if r.name == name]) > 1
            matched_geo_riding = None
            for geo_riding in geo_ridings[ro_year]:
                if (
                    not is_duplicate
                    and geo_riding.name
                    and (
                        geo_riding.name.lower() == name.lower()
                        or geo_riding.name == name.replace("--", "-")
                        or geo_riding.name.split("/")[0] == name
                    )
                ):
                    matched_geo_riding = geo_riding
                    break

                manual_match = corrections.get(geo_riding.id)
                if manual_match is None:
                    continue

                if not isinstance(manual_match, list):
                    manual_match = [manual_match]

                for match in manual_match:
                    if match["name"] == name and match["province"] == province:
                        matched_geo_riding = geo_riding
                        break

            if matched_geo_riding is None:

                if end_date_obj is None:
                    assert False, f"Could not find {name} in {ro_year}"
            else:
                geo_riding_by_year[ro_year] = matched_geo_riding

        if len(geo_riding_by_year) == 0:
            print(f"Could not find {name} in {ro_years}")
            continue

        riding = Riding(
            name,
            Province.from_name(province),
            start_date_obj,
            end_date_obj,
            {year: geo_riding.area for year, geo_riding in geo_riding_by_year.items()},
            center=(
                sum([r.shape.centroid.x for r in geo_riding_by_year.values()]) / len(geo_riding_by_year) / 1000,
                sum([r.shape.centroid.y for r in geo_riding_by_year.values()]) / len(geo_riding_by_year) / 1000,
            ),
        )
        data[Riding].append(riding)

        for year, geometry in geo_riding_by_year.items():
            for view_name in DetailViewName:
                if geometry.intersects(detail_map_polygons[view_name]):
                    riding_by_detail_view[view_name][year].append(riding)

            svg_dir = WEB_ARTIFACT_DIR / f"geometry/{riding.id()}/{year}"
            svg_dir.mkdir(parents=True, exist_ok=True)

            if not (svg_dir / "simple.svg").exists():
                with open(svg_dir / "simple.svg", "w") as f:
                    f.write(geometry.to_svg(1000))
            if not (svg_dir / "detailed.svg").exists():
                with open(svg_dir / "detailed.svg", "w") as f:
                    f.write(geometry.to_svg(100))

    for view_name, ridings_by_year in riding_by_detail_view.items():
        # print(view_name, ridings_by_year)
        data[DetailView].append(
            DetailView(
                view_name,
                ridings_by_year,
                DETAIL_MAP_BOUNDS[view_name]["x"],
                DETAIL_MAP_BOUNDS[view_name]["y"],
                DETAIL_MAP_BOUNDS[view_name]["width"],
                DETAIL_MAP_BOUNDS[view_name]["height"],
            )
        )

    print("Processing runs")
    candidates = {}
    runs_by_candidate = {}
    for row in election_and_candidate_rows:
        (
            picture_or_heading,
            province,
            riding,
            candidate,
            gender,
            occupation,
            party,
            result,
            votes,
        ) = row

        if picture_or_heading.startswith("Parliament: "):
            parliament = int(picture_or_heading[12:])
            data[Parliament].append(Parliament(parliament))

        elif picture_or_heading.startswith("Type of Election: "):
            election_type_str = picture_or_heading.split(": ")[1]
            election_type = {
                "By-Election": ElectionType.BYELECTION,
                "General": ElectionType.GENERAL,
            }[election_type_str]

        elif picture_or_heading.startswith("Date of Election: "):
            date = picture_or_heading[18:]
            year, month, day = date.split("-")
            date = datetime.date(int(year), int(month), int(day))
            data[Election].append(Election(date, election_type, data[Parliament][-1]))

        elif picture_or_heading == "":
            party = Party(party)
            data[Party].add(party)

            if (date, riding) == (datetime.date(2004, 6, 28), "Laurier--Sainte-Marie"):
                # https://en.wikipedia.org/wiki/Laurier%E2%80%94Sainte-Marie
                # Laurier—Sainte-Marie was abolished in 2003, then redistributed into Laurier and Holcheaga,
                # then Laurier was renamed to Laurier—Sainte-Marie in 2004 *after* the election.
                riding = "Laurier"
            elif (date, riding) == (
                datetime.date(2004, 6, 28),
                "Rimouski-Neigette--Témiscouata--Les Basques",
            ):
                # https://en.wikipedia.org/wiki/Rimouski-Neigette%E2%80%94T%C3%A9miscouata%E2%80%94Les_Basques
                # This riding was created as Rimouski--Témiscouata in 2003 and only renamed *after* the 2004 election.
                riding = "Rimouski--Témiscouata"

            matching_ridings = [
                r
                for r in data[Riding]
                if r.name == riding
                and r.province == Province.from_name(province)
                and date >= r.start_date
                and (r.end_date is None or date < r.end_date)
            ]
            if len(matching_ridings) != 1:
                print(matching_ridings)
                print(f"Could not find {riding} in {province} on {date}")

            assert len(matching_ridings) == 1
            riding_obj = matching_ridings[0]
fix duplicate candidates, see william mcdougall
            split_name = candidate.split(", ")
            last = split_name[0]
            first = "".join(split_name[1:])
            if first.isupper():
                first = first.title()
            if last.isupper():
                last = last.title()
            if (first, last, gender, occupation) == ("Chris", "d'Entremont", "Man", "Parliamentarian"):
                party = Party("Conservative Party of Canada")
                result = "Elected"
            elif (first, last, gender, occupation) == ("Chris", "d'Entremont", "Man", "Unemployed"):
                first = "Scott"
                last = "Spidle"
                party = Party("People's Party of Canada")
                result = "Defeated"
            elif (first, last, gender, occupation) == ("Joël", "Lightbound", "Man", "Sports Manager"):
                first = "Gilles"
                last = "Lépine"
                party = Party("Conservative Party of Canada")
                result = "Defeated"
            elif (first, last, gender, occupation) == ("Joël", "Lightbound", "Man", "Parliamentarian"):
                result = "Elected"

            candidate = Candidate(first, last, Gender.from_string(gender))
            first_first_name = first.split(" ")[0]
            key = (first_first_name, last)

            if key in candidates and candidates[key] != candidate:
                potential_match = candidates[key]
                potential_match_runs = runs_by_candidate[potential_match.id()]
                min_run_date = min([run.election.date for run in potential_match_runs])
                max_run_date = max([run.election.date for run in potential_match_runs])

                dates_match = date >= min_run_date and date <= max_run_date
                if date < min_run_date and min_run_date.year - date.year < 10:
                    dates_match = True
                elif date > max_run_date and date.year - max_run_date.year < 10:
                    dates_match = True

                potential_match_centers = [run.riding.center for run in potential_match_runs]
                average_center = (
                    sum([c[0] for c in potential_match_centers]) / len(potential_match_centers),
                    sum([c[1] for c in potential_match_centers]) / len(potential_match_centers),
                )
                distance = ((average_center[0] - riding_obj.center[0]) ** 2 + (average_center[1] - riding_obj.center[1]) ** 2) ** 0.5

                if distance < 40 and dates_match:
                    # Matched existing candidate!
                    candidate = candidates[key]

            candidates[key] = candidate

            run = Run(
                data[Election][-1],
                riding_obj,
                candidate,
                party,
                ElectionResult.from_string(result),
                int(votes),
                occupation,
            )
            data[Candidate].append(candidate)
            data[Run].append(run)
            runs_by_candidate.setdefault(candidate.id(), []).append(run)

            for election in data[Election]:
                if election.date == date:
                    election.runs.append(run.id())
                    break

        else:
            raise RuntimeError(f"Bad row: {row}")

    data[Candidate] = set(data[Candidate])

    for parliamentarian_row in parliamentarians_rows:
        name, record, _, _, riding, province, gender, party = parliamentarian_row
        if name.startswith("Count: "):
            continue
        last_name, first_name = name.split(", ")
        first_year, last_year = None, None
        for record_segment in record.split("\n"):
            if record_segment == "":
                continue

            parliamentarian_type, date_range = record_segment.split(" (")
            parliamentarian_type = ParliamentarianType.from_string(parliamentarian_type)

            date_range = date_range[:-1].split(" - ")
            start_date = date_range[0].split("/")
            end_date = date_range[1].split("/") if record_segment[1] else None
            start_date = datetime.date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
            if end_date is not None:
                if len(end_date) == 1:
                    if end_date[0] == "":
                        end_date = None
                    else:
                        end_date = datetime.date(int(end_date[0]), 1, 1)
                else:
                    end_date = datetime.date(int(end_date[0]), int(end_date[1]), int(end_date[2]))

            if first_year is None or start_date.year < first_year:
                first_year = start_date.year
            if end_date is not None and (last_year is None or end_date.year > last_year):
                last_year = end_date.year


    for run in data[Run]:
        run.candidate.runs.append(run.id())

    print("Writing JSON files")
    for cls, instances in data.items():
        obj = {}
        json_file = WEB_ARTIFACT_DIR / f"{cls.__name__.lower()}.json"
        for instance in instances:
            if instance.id() in obj:
                if (
                    isinstance(instance, Run)
                    and (instance.candidate.first_name, instance.candidate.last_name)
                    == ("John Angus", "MacLean")
                    and instance.election.date == datetime.date(1953, 8, 10)
                ):
                    continue
                else:
                    assert False, "Hash collision!"
            obj[instance.id()] = instance.to_json()
        print(f"Writing {json_file}")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False)
