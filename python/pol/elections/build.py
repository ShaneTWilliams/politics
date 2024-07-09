import datetime
import json
import xml

import geopandas
import openpyxl
from pol.elections.structures import *
from pol.paths import ARTIFACT_DIR, CACHE_DIR, SOURCES_DIR, PYTHON_PACKAGE_DIR

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
RIDING_YEARS = sorted([int(f.stem[6:10]) for f in GEOMETRY_DIR.glob("*.shp")])

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


def get_cached_geo_ridings():
    cache_file = CACHE_DIR / "geo_ridings.json"

    if cache_file.exists():
        with open(cache_file) as f:
            return json.load(f)

    ridings = {year: [] for year in RIDING_YEARS}

    debug_geo_ridings = []
    for year in RIDING_YEARS:
        print(year)
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

            simple_geometry = geometry.simplify(1000, preserve_topology=False)
            svg = simple_geometry.svg()
            xml_svg = xml.etree.ElementTree.fromstring(svg)
            for attr_key in ["fill", "stroke", "stroke-width", "opacity"]:
                xml_svg.attrib.pop(attr_key, None)
                for child in xml_svg:
                    child.attrib.pop(attr_key, None)
            final_svg = xml.etree.ElementTree.tostring(xml_svg).decode("utf-8")

            ridings[year].append({"name": name, "id": id, "geometry": final_svg})
            debug_geo_ridings.append(
                {"name": name, "id": id, "year": year, "copy": f"{id}: {{ # {name}"}
            )

    with open(ARTIFACT_DIR / "debug_geo_ridings.json", "w") as f:
        json.dump(debug_geo_ridings, f, indent=4, ensure_ascii=False)

    with open(cache_file, "w") as f:
        json.dump(ridings, f, indent=4, ensure_ascii=False)

    return ridings


def build():
    ARTIFACT_DIR.mkdir(exist_ok=True)

    ridings = get_cached_geo_ridings()

    election_and_candidate_rows = get_cached_xlsx(
        SOURCES_DIR / "electionsCandidates.xlsx", CACHE_DIR / "electionsCandidates.json"
    )
    riding_rows = get_cached_xlsx(
        SOURCES_DIR / "ridings/ParlInfoRidings1.xlsx", CACHE_DIR / f"ridings.json"
    )
    with open(PYTHON_PACKAGE_DIR / "elections/corrections.json", "r") as f:
        corrections = json.load(f)

    data = {
        Parliament: [],
        Election: [],
        Party: set(),
        Riding: [],
        Candidate: set(),
        Run: [],
    }

    print("Processing ridings")
    unassigned_ridings = []
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

        ro_years = [
            y
            for y in RIDING_YEARS
            if y >= start_date_obj.year
            and (end_date_obj is not None and y <= end_date_obj.year)
        ][:-1]

        for ro_year in ro_years:
            geometry = None
            is_duplicate = len([r for r in ridings[str(ro_year)] if r["name"] == name]) > 1

            for riding in ridings[str(ro_year)]:
                if (
                    not is_duplicate
                    and riding["name"]
                    and (
                        riding["name"].lower() == name.lower()
                        or riding["name"] == name.replace("--", "-")
                        or riding["name"].split("/")[0] == name
                    )
                ):
                    geometry = riding["geometry"]
                    break

                manual_match = corrections.get(riding["id"])
                if manual_match is None:
                    continue

                if not isinstance(manual_match, list):
                    manual_match = [manual_match]

                for match in manual_match:
                    if match["name"] == name and match["province"] == province:
                        geometry = riding["geometry"]
                        break

            if geometry is None:
                if name in (
                    "Saskatchewan",
                    "Saskatchewan (Provisional District)",
                    "Kitchener--Waterloo",
                    "Fort Nelson--Peace River",
                    "Charlotte",
                    "British Columbia Southern Interior",
                    "Barrie--Simcoe",
                    "Assiniboia East",  # https://en.wikipedia.org/wiki/Assiniboia_East
                    "Assiniboia West",
                    "Alberta (Provisional District)",
                    "Alberta",
                ):
                    continue
                unassigned_ridings.append(
                    {
                        "name": name,
                        "province": province,
                        "start_date": {
                            "year": start_date_obj.year,
                            "month": start_date_obj.month,
                            "day": start_date_obj.day,
                        },
                        "end_date": {
                            "year": end_date_obj.year,
                            "month": end_date_obj.month,
                            "day": end_date_obj.day,
                        },
                        "ro_year": ro_year,
                    }
                )
                # assert False, f"Unassigned riding: {name} ({province})"

            province_enum = Province.from_name(province)
            data[Riding].append(
                Riding(name, province_enum, geometry, start_date_obj, end_date_obj)
            )

    print(f"Unassigned ridings: {len(unassigned_ridings)}")
    new_corrections = {}
    with open(PYTHON_PACKAGE_DIR / "elections/corrections.json", "r") as f:
        old_corrections = json.load(f)

    def add_to_corrections(geo_name, geo_id, ec_name, ec_province, corrections):
        new_entry = {"name": ec_name, "province": ec_province, "geo_name": geo_name}
        if geo_id in corrections:
            old_entry = corrections[geo_id]
            if isinstance(old_entry, list):
                old_entry.append(new_entry)
            else:
                corrections[geo_id] = [old_entry, new_entry]
        else:
            corrections[geo_id] = new_entry

    import curses
    def run_labeler(stdscr, ridings, unassigned_ridings):
        ur_index = 0
        geo_index = 0
        selected = ""

        PROVINCE_CODES = {
            "10": "Newfoundland and Labrador",
            "11": "Prince Edward Island",
            "12": "Nova Scotia",
            "13": "New Brunswick",
            "24": "Quebec",
            "35": "Ontario",
            "46": "Manitoba",
            "47": "Saskatchewan",
            "48": "Alberta",
            "59": "British Columbia",
            "60": "Yukon",
            "61": "Northwest Territories",
            "62": "Nunavut",
        }

        unassigned_ridings = [r for r in unassigned_ridings if r["ro_year"] != 2003]
        curses.curs_set(0)
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            ur = unassigned_ridings[ur_index]
            year_ridings = sorted(ridings[str(ur['ro_year'])], key=lambda r: r["name"])
            province_ridings = [r for r in year_ridings if PROVINCE_CODES[r["id"][4:6]] == ur["province"]]

            start_date = f"{ur['start_date']['year']}-{ur['start_date']['month']}-{ur['start_date']['day']}"
            end_date = f"{ur['end_date']['year']}-{ur['end_date']['month']}-{ur['end_date']['day']}"
            stdscr.addstr(
                0, 0,
                f"{ur['name']}, {ur['province']}  |  {start_date} - {end_date}  |  {ur['ro_year']}",
                curses.A_BOLD | curses.A_UNDERLINE
            )

            middle = (height // 2) - 1
            for y in range(2, height):
                list_index = max(min(geo_index + y - 1 - middle, len(province_ridings)), -1)
                if list_index == len(province_ridings):
                    break
                elif list_index < 0:
                    continue
                attr = curses.A_STANDOUT if list_index == geo_index else curses.A_NORMAL
                geo_riding = province_ridings[list_index]
                check = "✓" if (geo_riding["id"] in new_corrections and new_corrections[geo_riding["id"]]["name"] == ur["name"]) else " "
                stdscr.addstr(y, 0, f"{check} {geo_riding["name"]}", attr)

            ch = stdscr.getch()
            if ch == curses.KEY_RIGHT:
                ur_index = min(len(unassigned_ridings) - 1, ur_index + 1)
            elif ch == curses.KEY_LEFT:
                ur_index = max(0, ur_index - 1)
            elif ch == curses.KEY_UP:
                geo_index = max(0, geo_index - 1)
            elif ch == curses.KEY_DOWN:
                geo_index = min(len(province_ridings) - 1, geo_index + 1)
            elif ch == curses.KEY_PPAGE:
                geo_index = max(0, geo_index - 10)
            elif ch == curses.KEY_NPAGE:
                geo_index = min(len(province_ridings) - 1, geo_index + 10)
            elif ch == ord(" "):
                geo_riding = province_ridings[geo_index]
                for k, v in new_corrections.copy().items():
                    if v["name"] == ur["name"] and v["province"] == ur["province"] and k[:4] == str(ur["ro_year"]):
                        new_corrections.pop(k)

                add_to_corrections(
                    geo_riding["name"],
                    geo_riding["id"],
                    ur["name"],
                    ur["province"],
                    new_corrections,
                )

    try:
        curses.wrapper(run_labeler, ridings, unassigned_ridings)
    except KeyboardInterrupt:
        pass

    print(f"New corrections: {new_corrections}")
    for k, v in new_corrections.items():
        add_to_corrections(
            v["geo_name"],
            k,
            v["name"],
            v["province"],
            old_corrections,
        )
    with open(PYTHON_PACKAGE_DIR / "elections/corrections.json", "w") as f:
        json.dump(old_corrections, f, indent=4, ensure_ascii=False, sort_keys=True)

    exit(0)
    print("Processing runs")
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
            party = Party(party, PARTY_COLORS.get(party, None))
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
                # print(date, riding, province, candidate.first_name, candidate.last_name )
                # print(matching_ridings)
                # for r in matching_ridings:
                #    print(r.name, r.province, r.start_date, r.end_date)
                continue
            assert len(matching_ridings) == 1

            run = Run(
                data[Election][-1],
                matching_ridings[0],
                candidate,
                party,
                ElectionResult.from_string(result),
                int(votes),
            )
            data[Run].append(run)

            for election in data[Election]:
                if election.date == date:
                    election.runs.append(run.id())
                    break

        else:
            raise RuntimeError(f"Bad row: {row}")

    print("Writing JSON files")
    for cls, instances in data.items():
        obj = {}
        for instance in instances:
            obj[instance.id()] = instance.to_json()
        json_file = ARTIFACT_DIR / f"{cls.__name__.lower()}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=4, ensure_ascii=False)
