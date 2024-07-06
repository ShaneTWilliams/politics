import geopandas
import json
import xml
import datetime

import openpyxl

from pol.paths import SOURCES_DIR, ARTIFACTS_DIR, CACHE_DIR
from pol.build.data import *

BAD_DISTRICTS = [
    # B.C.
    "Vancouver",
    "Victoria (B.C.)",
    "New Westminster",
    "Cariboo",
    "Yale",

    # Manitoba
    "Lisgar",
    "Provencher",
    "Selkirk",
    "Marquette",
]

PARTY_COLORS = {
    "Liberal Party of Canada": Color.RED,
    "Anti-Confederate": Color.ORANGE,
    "Conservative (1867-1942)": Color.BLUE,
    "Liberal-Conservative": Color.PURPLE,
}

# Keys are the geo dataset's "fedid" field.
# Comments are the name in the geo dataset
# "name" tag is the name in the EC dataset.
# "province" tag is the province in the EC dataset.

# For early BC districts, the "District" suffix was
# removed in 1971 with the ridings remaining identical.
# https://en.wikipedia.org/wiki/New_Westminster_District
GEO_ID_TO_EC_RIDINGS = {
    186713013: {  # Victoria (N.B.)
        "name": "Victoria",
        "province": "New Brunswick",
    },
    186759004: [  # Victoria (B.C.)
        {
            "name": "Victoria",
            "province": "British Columbia",
        },
        {
            "name": "Victoria District",
            "province": "British Columbia",
        }
    ],
    186712017: {   # Victoria (N.S.)
        "name": "Victoria",
        "province": "Nova Scotia",
    },
    186724061: {  # Trois-Rivières
        "name": "Three Rivers",
        "province": "Quebec",
    },
    186724062: {  # Deux-Montagnes
        "name": "Two Mountains",
        "province": "Quebec",
    },
    186759005: {  # Yale
        "name": "Yale District",
        "province": "British Columbia",
    },
    186759003: {  # Vancouver
        "name": "Vancouver Island",
        "province": "British Columbia",
    },
    186724057: {  # Saint-Jean
        "name": "St. John's",
        "province": "Quebec",
    },
    186713004: {  # City and County of St. John
        "name": "St. John (City and County of)",
        "province": "New Brunswick",
    },
    186713005: {  # City of St. John
        "name": "St. John (City of )",
        "province": "New Brunswick",
    },
    186724056: {  # Saint-Hyacinthe
        "name": "St. Hyacinthe",
        "province": "Quebec",
    },
    186724054: {  # Sherbrooke
        "name": "Sherbrooke (Town of)",
        "province": "Quebec",
    },
    186724052: {  # Saint-Maurice
        "name": "Saint Maurice",
        "province": "Quebec",
    },
    186712014: {  # Queens
        "name": "Queen's",
        "province": "New Brunswick",
    },
    186713010: {  # Queens
        "name": "Queens",
        "province": "Nova Scotia",
    },
    186724047: {  # Québec-Centre
        "name": "Quebec-Centre",
        "province": "Quebec",
    },
    186724045: { # Québec-Est
        "name": "Quebec East",
        "province": "Quebec",
    },
    186724046: { # Québec-Ouest
        "name": "Quebec West",
        "province": "Quebec",
    },
    186724044: {  # Québec (Comté)
        "name": "Quebec County",
        "province": "Quebec",
    },
    186724041: {  # Ottawa
        "name": "Ottawa (City of)",
        "province": "Ontario",
    },
    186735052: {  # Ottawa
        "name": "Ottawa (County of)",
        "province": "Quebec",
    },
    186759002: {  # New Westminster
        "name": "New Westminster District",
        "province": "British Columbia",
    },
    186724038: {  # Montreal Ouest
        "name": "Montreal West",
        "province": "Quebec",
    },
    186724037: {  # Montreal Est
        "name": "Montreal East",
        "province": "Quebec",
    },
    186712011: {  # Kings (N.S.)
        "name": "Kings",
        "province": "Nova Scotia",
    },
    186713008: {  # Kings (N.B.)
        "name": "King's",
        "province": "New Brunswick",
    },
    186735031: {  # Kent (Ont.)
        "name": "Kent",
        "province": "Ontario",
    },
    186713007: {  # Kent (N.B.)
        "name": "Kent",
        "province": "New Brunswick",
    },
    186724021: {  # Jacques-Cartier
        "name": "Jacques Cartier",
        "province": "Quebec",
    },
    186735010: {  # Carleton (Ont.)
        "name": "Carleton",
        "province": "Ontario",
    },
    186713002: {  # Carleton (N.B.)
        "name": "Carleton",
        "province": "New Brunswick",
    },
    186759001: {  # Cariboo
        "name": "Cariboo District",
        "province": "British Columbia",
    }
}

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

def build():
    ARTIFACTS_DIR.mkdir(exist_ok=True)

    geometry_dir = SOURCES_DIR / "geometry/fedshapes_cbf_20221003"
    riding_years = sorted([int(f.stem[6:10]) for f in geometry_dir.glob("*.shp")])
    ridings = {year: [] for year in riding_years}

    for year in riding_years:
        print(year)
        gdf = geopandas.read_file(SOURCES_DIR / f"geometry/fedshapes_cbf_20221003/CBF_RO{year}_CSRS.shp", engine='pyogrio')

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

            simple_geometry = geometry.simplify(1000, preserve_topology=False)
            svg = simple_geometry.svg()
            xml_svg = xml.etree.ElementTree.fromstring(svg)
            for attr_key in ["fill", "stroke", "stroke-width", "opacity"]:
                xml_svg.attrib.pop(attr_key, None)
                for child in xml_svg:
                    child.attrib.pop(attr_key, None)
            final_svg = xml.etree.ElementTree.tostring(xml_svg).decode("utf-8")

            ridings[year].append({
                "name": name,
                "id": id,
                "geometry": final_svg
            })

    election_and_candidate_rows = get_cached_xlsx(
        SOURCES_DIR / "electionsCandidates.xlsx",
        CACHE_DIR / "electionsCandidates.json"
    )
    riding_rows = get_cached_xlsx(
        SOURCES_DIR / "ridings/ParlInfoRidings1.xlsx",
        CACHE_DIR / f"ridings.json"
    )

    data = {
        Parliament: [],
        Election: [],
        Party: set(),
        Riding: [],
        Candidate: set(),
        Run: [],
    }

    print("a")
    for row in riding_rows:
        name, province, region, start_date, end_date, status = row
        if start_date == "":
            start_date_obj = None
        else:
            start_year, start_month, start_day = start_date.split("-")
            start_date_obj = datetime.date(int(start_year), int(start_month), int(start_day))

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

        most_recent_year = min(ridings.keys())
        for year in ridings.keys():
            if 0 <= start_date_obj.year - year < most_recent_year:
                most_recent_year = year

        geometry = None
        is_duplicate = len([r for r in ridings[most_recent_year] if r["name"] == name]) > 1
        for riding in ridings[most_recent_year]:
            if not is_duplicate and riding["name"] == name:
                geometry = riding["geometry"]
                break

            manual_match = GEO_ID_TO_EC_RIDINGS.get(int(riding["id"]))
            if manual_match is None:
                continue

            if not isinstance(manual_match, list):
                manual_match = [manual_match]

            for match in manual_match:
                if match["name"] == name and match["province"] == province:
                    geometry = riding["geometry"]
                    break

        # if geometry is None:
        #     print(f"N: {name} {province}")

        province_enum = Province.from_name(province)
        data[Riding].append(Riding(name, province_enum, geometry, start_date_obj, end_date_obj))

    print("b")
    for row in election_and_candidate_rows:
        picture_or_heading, province, riding, candidate, gender, occupation, party, result, votes = row

        if picture_or_heading.startswith("Parliament: "):
            parliament = int(picture_or_heading[12:])
            data[Parliament].append(Parliament(parliament))

        elif picture_or_heading.startswith("Type of Election: "):
            election_type_str =  picture_or_heading.split(": ")[1]
            election_type = {
                "By-Election": ElectionType.BYELECTION,
                "General": ElectionType.GENERAL,
            }[election_type_str]

        elif picture_or_heading.startswith("Date of Election: "):
            date = picture_or_heading[18:]
            year, month, day = date.split("-")
            date = datetime.date(int(year), int(month), int(day))
            data[Election].append(
                Election(date, election_type, data[Parliament][-1])
            )

        elif picture_or_heading == "":
            party = Party(party, PARTY_COLORS.get(party, "000000"))
            data[Party].add(party)

            split_name = candidate.split(", ")
            last = split_name[0]
            first = "".join(split_name[1:])
            candidate = Candidate(first, last, gender, occupation)
            data[Candidate].add(candidate)

            if (date, riding) == (datetime.date(2004, 6, 28), "Laurier--Sainte-Marie"):
                # https://en.wikipedia.org/wiki/Laurier%E2%80%94Sainte-Marie
                # Laurier—Sainte-Marie was abolished in 2003, then redistributed into Laurier and Holcheaga,
                # then Laurier was renamed to Laurier—Sainte-Marie in 2004 *after* the election.
                riding = "Laurier"
            elif (date, riding) == (datetime.date(2004, 6, 28), "Rimouski-Neigette--Témiscouata--Les Basques"):
                # https://en.wikipedia.org/wiki/Rimouski-Neigette%E2%80%94T%C3%A9miscouata%E2%80%94Les_Basques
                # This riding was created as Rimouski--Témiscouata in 2003 and only renamed *after* the 2004 election.
                riding = "Rimouski--Témiscouata"

            matching_ridings = [
                r for r in data[Riding] if r.name == riding and \
                    r.province == Province.from_name(province) and \
                    date >= r.start_date and \
                    (r.end_date is None or date < r.end_date)
            ]

            assert len(matching_ridings) == 1

            run = Run(
                data[Election][-1],
                matching_ridings[0],
                candidate,
                party,
                ElectionResult.from_string(result),
                int(votes)
            )
            data[Run].append(run)
            for election in data[Election]:
                if election.date == date:
                    election.runs.append(run.id())
                    break

        else:
            raise RuntimeError(f"Bad row: {row}")

    print("d")
    for cls, instances in data.items():
        obj = {}
        for instance in instances:
            obj[instance.id()] = instance.to_json()
        json_file = ARTIFACTS_DIR / f"{cls.__name__.lower()}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=4, ensure_ascii=False)
