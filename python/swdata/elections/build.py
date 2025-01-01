import datetime
import json
import os
import pickle

import geopandas
import openpyxl
from alive_progress import alive_bar
from swdata.elections.constants import DETAIL_MAP_BOUNDS
from swdata.elections.patches import (
    CANDIDATE_INFO_PATCHES,
    CANDIDATE_SPLIT_EXCEPTIONS,
    GEOMETRY_TO_RIDING_METADATA,
    RIDING_NAME_CHANGES_BY_DATE,
    RIDING_NAME_PATCHES,
    PARTY_PATCHES,
)
from swdata.elections.structures import *
from swdata.paths import (
    ARTIFACT_DIR,
    CACHE_DIR,
    GEOMETRY_ARTIFACT_DIR,
    GEOMETRY_DIR,
    SOURCES_DIR,
    WEB_ARTIFACT_DIR,
    ELECTION_SUMMARY_JSON,
    RIDING_SUMMARY_JSON,
)
from shapely.geometry import Polygon

RO_YEARS = sorted([int(f.stem[6:10]) for f in GEOMETRY_DIR.glob("*.shp")])

__unique_id = 0


def get_uid():
    global __unique_id
    __unique_id += 1
    return __unique_id


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
        geo_cache_file = CACHE_DIR / f"CBF_RO{year}_CSRS.pkl"
        if geo_cache_file.exists():
            with open(geo_cache_file, "rb") as f:
                gdf = pickle.load(f)
        else:
            gdf = geopandas.read_file(
                GEOMETRY_DIR / f"CBF_RO{year}_CSRS.shp",
                engine="pyogrio",
            )
            with open(geo_cache_file, "wb") as f:
                pickle.dump(gdf, f)

        # Columns are... inconsistent
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


def generate_ridings(riding_rows, geometry_by_year):
    with open(RIDING_SUMMARY_JSON, "r") as f:
        riding_summaries = json.load(f)
    ridings = []
    for row in riding_rows:
        name, province, region, start_date, end_date, status = row
        if name == "Barrie--Simcoe":
            # Data error TODO
            continue

        if start_date == "":
            start_date_obj = None
        else:
            year, month, day = start_date.split("-")
            start_date_obj = datetime.date(int(year), int(month), int(day))

        if end_date == "":
            end_date_obj = None
        else:
            year, month, day = end_date.split("-")
            end_date_obj = datetime.date(int(year), int(month), int(day))

        # According to EC these ridings started on May 1st, 1871.
        # But these elections were held on March 2nd and 3rd, 1871
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

        if end_date_obj is not None:
            ro_years.pop(0)

        riding_geometry_by_year = {}
        for ro_year in ro_years:
            match = None

            # See if we can find an exact match by name
            for geometry in geometry_by_year[ro_year]:
                if geometry.name and (
                    geometry.name.lower() == name.lower()
                    or geometry.name == name.replace("--", "-")
                    or geometry.name.split("/")[0] == name
                ):
                    match = geometry
                    break

            # Otherwise, try to find a match using a manual patch table
            if match is None:
                for geometry in geometry_by_year[ro_year]:
                    manual_matches = GEOMETRY_TO_RIDING_METADATA.get(
                        int(geometry.id_num), []
                    )
                    if not isinstance(manual_matches, list):
                        manual_matches = [manual_matches]
                    for manual_match in manual_matches:
                        if (
                            manual_match["name"] == name
                            and manual_match["province"] == province
                        ):
                            match = geometry
                            break

            # Still nothing
            if match is None:
                assert False, f"Could not find {name} in {ro_year}"

            riding_geometry_by_year[ro_year] = match

        summary_data = riding_summaries[province].get(name.replace("--", "—"), None)
        ridings.append(
            Riding(
                name,
                Province.from_name(province),
                start_date_obj,
                end_date_obj,
                riding_geometry_by_year,
                None if summary_data is None else summary_data["summary"],
                None if summary_data is None else summary_data["url"],
            )
        )

    for riding in sorted(ridings, key=lambda r: r.start_date, reverse=True):
        if riding.end_date in RIDING_NAME_CHANGES_BY_DATE:
            rename_start_date = riding.end_date + datetime.timedelta(days=1)
            rename_name = RIDING_NAME_CHANGES_BY_DATE[riding.end_date][riding.name]
            rename_start_date = {
                "Timiskaming--French River": datetime.date(1990, 12, 19),
                "Berthier--Maskinongé": datetime.date(1975, 3, 13),
                "Middlesex--London--Lambton": datetime.date(1974, 5, 7),
                "Nanaimo--Cowichan--The Islands": datetime.date(1962, 4, 18),
                "Northwest Territories": datetime.date(1962, 3, 23),
            }.get(rename_name, rename_start_date)
            renamed_riding = [
                r
                for r in ridings
                if r.name == rename_name and r.start_date == rename_start_date
            ].pop()
            rename_ro_year = [y for y in RO_YEARS if y < riding.end_date.year][-1]
            riding.geometry_by_year[rename_ro_year] = renamed_riding.geometry_by_year[
                rename_ro_year
            ]

    print(len(ridings))
    print(len([r for r in ridings if r.summary != None]))
    return ridings


def generate_detail_views(ridings):
    detail_views = []
    for city, bounds in DETAIL_MAP_BOUNDS.items():
        detail_view = DetailView(
            city,
            {},
            bounds["x"],
            bounds["y"],
            bounds["width"],
            bounds["height"],
        )
        for riding in ridings:
            polygon = Polygon(
                [
                    (bounds["x"], bounds["y"]),
                    (bounds["x"] + bounds["width"], bounds["y"]),
                    (bounds["x"] + bounds["width"], bounds["y"] - bounds["height"]),
                    (bounds["x"], bounds["y"] - bounds["height"]),
                ]
            )
            for year, geometry in riding.geometry_by_year.items():
                if geometry.shape.intersects(polygon):
                    detail_view.ridings_by_year.setdefault(year, []).append(riding)
        detail_views.append(detail_view)

    return detail_views


def split_candidates_by_year(candidates_by_id):
    new_candidates = []
    remove_candidates = []
    SPLIT_THRESHOLD = datetime.timedelta(days=30 * 365)
    MANUAL_SPLITS = {
        ("Moore", "Christine"): [2006],
        ("Clark", "Charles Joseph"): [2000],
    }

    # Split based on time
    for candidate in candidates_by_id.values():
        if (candidate.first_name, candidate.last_name) in CANDIDATE_SPLIT_EXCEPTIONS:
            continue

        sorted_runs = sorted(candidate.runs, key=lambda run: run.election.date)
        should_be_split = False
        for i in range(1, len(sorted_runs)):
            if (sorted_runs[i].election.date - sorted_runs[i - 1].election.date) > SPLIT_THRESHOLD \
                or (candidate.last_name, candidate.first_name) in MANUAL_SPLITS:
                should_be_split = True
                break

        if not should_be_split:
            continue

        candidate_run_groups = []
        for run in sorted_runs:
            if (
                not candidate_run_groups
                or (run.election.date - candidate_run_groups[-1][-1].election.date) > SPLIT_THRESHOLD
                or run.election.date.year in MANUAL_SPLITS.get((candidate.last_name, candidate.first_name), [])
            ):
                candidate_run_groups.append([])
            candidate_run_groups[-1].append(run)

        for group in candidate_run_groups:
            new_candidate = Candidate(
                candidate.first_name,
                candidate.last_name,
                candidate.gender,
                index=get_uid(),  # TODO: Hack of all time
            )
            new_candidate.runs = group
            for run in group:
                run.candidate = new_candidate
            new_candidates.append(new_candidate)
        remove_candidates.append(candidate)

    for candidate in remove_candidates:
        del candidates_by_id[candidate.id()]
    for new_candidate in new_candidates:
        candidates_by_id[new_candidate.id()] = new_candidate


def split_candidates_by_province(candidates_by_id):
    new_candidates = []
    remove_candidates = []
    for candidate in candidates_by_id.values():
        if (candidate.first_name, candidate.last_name) in CANDIDATE_SPLIT_EXCEPTIONS:
            continue

        candidate_provinces = set([r.riding.province for r in candidate.runs])
        if len(candidate_provinces) == 1:
            continue

        for province in candidate_provinces:
            province_runs = [r for r in candidate.runs if r.riding.province == province]
            new_candidate = Candidate(
                candidate.first_name,
                candidate.last_name,
                candidate.gender,
                index=get_uid(),  # TODO: Hack of all time
            )
            new_candidate.runs = province_runs
            for run in province_runs:
                run.candidate = new_candidate
            new_candidates.append(new_candidate)
        remove_candidates.append(candidate)

    for candidate in remove_candidates:
        del candidates_by_id[candidate.id()]
    for new_candidate in new_candidates:
        candidates_by_id[new_candidate.id()] = new_candidate


def generate_runs(election_and_candidate_rows, ridings):
    with open(ELECTION_SUMMARY_JSON, "r") as f:
        summaries = json.load(f)
    maclean_found = False  # lol
    elections, runs = [], []
    parties = set()
    candidates_by_id = {}
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

        elif picture_or_heading.startswith("Type of Election: "):
            election_type_str = picture_or_heading.split(": ")[1]
            election_type = ElectionType.from_string(election_type_str)
            current_riding = None

        elif picture_or_heading.startswith("Date of Election: "):
            date = picture_or_heading[18:]
            year, month, day = date.split("-")
            date = datetime.date(int(year), int(month), int(day))
            if election_type == ElectionType.GENERAL:
                elections.append(Election(date, election_type, parliament, summary=summaries[str(date.year)]))

        elif picture_or_heading == "":
            party = PARTY_PATCHES.get(party, party)
            party_obj = Party(party)
            parties.add(party_obj)

            riding = RIDING_NAME_PATCHES.get((date, riding), riding)

            matching_ridings = [
                r
                for r in ridings
                if r.name == riding
                and r.province == Province.from_name(province)
                and date >= r.start_date
                and (r.end_date is None or date < r.end_date)
            ]

            assert len(matching_ridings) == 1
            riding_obj = matching_ridings[0]

            if election_type == ElectionType.BYELECTION and current_riding != riding:
                elections.append(
                    Election(date, election_type, parliament, riding=riding_obj)
                )  # By-election
                current_riding = riding

            split_name = candidate.split(", ")
            last = split_name[0].strip()
            first = "".join(split_name[1:]).strip().replace("  ", " ")
            if first.isupper():
                first = first.title()
            if last.isupper():
                last = last.title()

            patch = CANDIDATE_INFO_PATCHES.get((first, last, gender, occupation), None)
            if patch is not None:
                first = patch.get("first", first)
                last = patch.get("last", last)
                gender = patch.get("gender", gender)
                occupation = patch.get("occupation", occupation)

            candidate_obj = Candidate(first, last, Gender.from_string(gender))
            if candidate_obj.id() in candidates_by_id:
                candidate_obj = candidates_by_id[candidate_obj.id()]
            else:
                candidates_by_id[candidate_obj.id()] = candidate_obj

            if (
                not maclean_found
                and candidate_obj == Candidate("John Angus", "MacLean", Gender.MALE)
                and date == datetime.date(1953, 8, 10)
            ):
                continue

            run = Run(
                elections[-1],
                riding_obj,
                candidate_obj,
                party_obj,
                ElectionResult.from_string(result),
                int(votes),
                occupation,
            )
            runs.append(run)
            run.election.runs.append(run)

        else:
            raise RuntimeError(f"Bad row: {row}")

    for run in runs:
        run.candidate.runs.append(run)
        if run.result in (ElectionResult.ELECTED, ElectionResult.ACCLAIMED, ElectionResult.ELECTED_COURT_DECISION):
            for party in parties:
                if run.party.name == party.name:
                    party.has_won_election = True
                    break

    split_candidates_by_province(candidates_by_id)
    split_candidates_by_year(candidates_by_id)

    candidates = list(candidates_by_id.values())

    return runs, candidates, elections, parties


def generate_parliaments(parliament_rows, parties, candidates):
    current_parliament = None
    ret = []
    for row in parliament_rows:
        if row[0].startswith("Parliament: "):
            current_parliament = int(row[0][12:])
            continue

        dates, length, sessions, throne_speeches, budgets, senate_noms, _, gov_type, gov_parties, prime_ministers, oppo_leaders, oppo_parties = row
        if " - " in dates:
            start_date, end_date = dates.split(" - ")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            start_date = dates
            end_date = None
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        gov_type = GovernmentType.from_string(gov_type)

        def get_parties_from_list(party_list):
            ret = set()
            for party_str in party_list.split("\n"):
                if party_str == "":
                    continue
                party_name = party_str.split(" (")[0]
                party_name = PARTY_PATCHES.get(party_name, party_name)

                for party_obj in parties:
                    if party_obj.name == PartyName.from_name(party_name):
                        ret.add(party_obj)
            return list(ret)

        def get_candidates_from_list(candidate_list, valid_parties):
            #not getting the right john a macdonald here, need to match on more than just first and last name.
            ret = set()
            for candidate_str in candidate_list.split("\n"):
                if candidate_str == "":
                    continue
                last, first = candidate_str.split(" (")[0].split(", ")
                last = last.strip()
                first = first.strip()
                for candidate in candidates:
                    if candidate.first_name == first and candidate.last_name == last:
                        # get the run right before the start of this parliament
                        for run in candidate.runs:
                            if run.party in valid_parties \
                                and run.result in [ElectionResult.ELECTED, ElectionResult.ACCLAIMED, ElectionResult.ELECTED_COURT_DECISION] \
                                and run.election.date + datetime.timedelta(days=365) > start_date \
                                and (end_date is None or run.election.date <= end_date):
                                ret.add(candidate)
                                break
            return list(ret)

        gov_parties = get_parties_from_list(gov_parties)
        oppo_parties = get_parties_from_list(oppo_parties)
        prime_ministers = get_candidates_from_list(prime_ministers, gov_parties)
        oppo_leaders = get_candidates_from_list(oppo_leaders, oppo_parties)

        ret.append(Parliament(
            current_parliament,
            start_date,
            end_date,
            gov_parties=gov_parties,
            prime_ministers=prime_ministers,
            oppo_parties=oppo_parties,
            oppo_leaders=oppo_leaders,
            government_type=gov_type,
            sessions=int(sessions),
            throne_speeches=int(throne_speeches),
            budgets=int(budgets),
            senate_nominations=int(senate_noms),
        ))

    return ret


def build():
    ARTIFACT_DIR.mkdir(exist_ok=True)
    CACHE_DIR.mkdir(exist_ok=True)

    print("Loading data")
    election_and_candidate_rows = get_cached_xlsx(
        SOURCES_DIR / "electionsCandidates.xlsx", CACHE_DIR / "electionsCandidates.json"
    )
    riding_rows = get_cached_xlsx(
        SOURCES_DIR / "ParlinfoRidings.xlsx", CACHE_DIR / f"ridings.json"
    )
    parliamentarians_rows = get_cached_xlsx(
        SOURCES_DIR / "Parliamentarians.xlsx", CACHE_DIR / f"parliamentarians.json"
    )
    parliament_rows = get_cached_xlsx(
        SOURCES_DIR / "Parliaments.xlsx", CACHE_DIR / f"parliaments.json"
    )


    data = {
        Parliament: [],
        Election: [],
        Party: set(),
        Riding: [],
        Run: [],
        DetailView: [],
        Candidate: [],
        Geometry: [],
    }

    print("Loading geometry")
    geometry_by_year = load_geo_ridings()
    data[Geometry] = set([g for year in geometry_by_year.values() for g in year])

    print("Generating ridings")
    data[Riding] = generate_ridings(riding_rows, geometry_by_year)

    print("Generating detail views")
    data[DetailView] = generate_detail_views(data[Riding])

    print("Processing runs")
    data[Run], data[Candidate], data[Election], data[Party] = (
        generate_runs(election_and_candidate_rows, data[Riding])
    )

    print("Processing parliaments")
    data[Parliament] = generate_parliaments(parliament_rows, data[Party], data[Candidate])

    print("Processing parliamentarians")
    for parliamentarian_row in parliamentarians_rows:
        name, record, _, _, riding, province, gender, party = parliamentarian_row
        if name.startswith("Count: "):
            continue

        last_name, first_name = name.replace("  ", " ").split(", ")

        if (first_name, last_name) == ("Bob", "Rae"):
            first_name = "Robert (Bob) Keith"
        elif (first_name, last_name) == ("John G.", "Williams"):
            first_name = "John Glass"

        matching_candidates = [
            c
            for c in data[Candidate]
            if c.first_name == first_name and c.last_name == last_name
        ]

        if len(matching_candidates) > 1:
            for c in matching_candidates:
                match_provinces = set([r.riding.province for r in c.runs])
                parl_provinces = set([Province.from_name(province.split("\n")[0])])
                if (
                    len(match_provinces) == 1
                    and len(parl_provinces) == 1
                    and match_provinces.pop() == parl_provinces.pop()
                ):
                    matching_candidates = [c]
                    break

            if len(matching_candidates) > 1:
                if (first_name, last_name) == ("John", "Herron"):
                    matching_candidates = [
                        c
                        for c in matching_candidates
                        if c.runs[0].election.date.year == 1904
                    ]
                elif (first_name, last_name) == ("William Dell", "Perley"):
                    matching_candidates = [
                        c
                        for c in matching_candidates
                        if c.runs[0].election.date.year == 1887
                    ]

            if len(matching_candidates) > 1:
                print(f"Multiple candidates for {first_name} {last_name}")
                continue

    print("Writing geometry")
    for geometry in data[Geometry]:
        svg_dir = GEOMETRY_ARTIFACT_DIR / f"{geometry.id()}"
        svg_dir.mkdir(parents=True, exist_ok=True)

        if not (svg_dir / "simple.svg").exists():
            with open(svg_dir / "simple.svg", "w") as f:
                f.write(geometry.to_svg(1000))
        if not (svg_dir / "detailed.svg").exists():
            with open(svg_dir / "detailed.svg", "w") as f:
                f.write(geometry.to_svg(100))

    print("Writing JSON files")
    WEB_ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    with alive_bar(len(data), elapsed=False, stats=False) as bar:
        for cls, instances in data.items():
            fields = set()
            json_file = WEB_ARTIFACT_DIR / f"{cls.__name__.lower()}.json"
            fields_json_file = WEB_ARTIFACT_DIR / f"{cls.__name__.lower()}_fields.json"

            bar()
            bar.text(json_file.name)

            obj = {}
            for instance in instances:
                if instance.id() in obj:
                    assert False, "Hash collision!"
                instance_json = instance.to_json()
                fields.update(instance_json.keys())
                obj[instance.id()] = [instance_json[k] for k in sorted(instance_json)]

            with open (fields_json_file, "w") as f:
                json.dump(sorted(list(fields)), f)

            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(obj, f, ensure_ascii=False)
