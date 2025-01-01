import wikipediaapi
import json
import datetime
from swdata.paths import SOURCES_DIR

USER_AGENT = "Shane Williams' Python bot (shanethomaswilliams@gmail.com)"

GENERAL_ELECTION_SUMMARY_FILE = SOURCES_DIR / "election_summaries.json"
RIDING_SUMMARY_FILE = SOURCES_DIR / "riding_summaries.json"

PROVINCES = [
    "Alberta",
    "British Columbia",
    "Manitoba",
    "New Brunswick",
    "Newfoundland and Labrador",
    "Nova Scotia",
    "Ontario",
    "Prince Edward Island",
    "Quebec",
    "Saskatchewan",
    "Northwest Territories",
    "Nunavut",
    "Yukon"
]

STRINGS_TO_IGNORE = [
    "Category:",
    "Canadian federal election results in ",
    "List of ",
    "electoral districts"
]

SUFFIXES_TO_REMOVE = [
    " (electoral district)",
    " (federal electoral district)",
    " (Canadian electoral district)",
    " ({province} federal electoral district)",
    " ({province} electoral district)",
]


def build():
    wiki = wikipediaapi.Wikipedia(USER_AGENT, "en")

    summaries = {}
    p = wiki.page("Category:Canadian federal elections by year")
    current_year = datetime.datetime.now().year
    for page_name, page in p.categorymembers.items():
        if page_name.startswith("Category:") or not page_name.endswith("Canadian federal election"):
            continue

        year = int(page_name.split(" ")[0])
        if year < current_year:
            print(f"Getting summary for {year} election")
            summaries[year] = page.summary.split("\n")

    with open(GENERAL_ELECTION_SUMMARY_FILE, "w") as f:
        json.dump(summaries, f, indent=4)

    riding_pages = {}
    for province in PROVINCES:
        province_pages = {}

        current_name = f"Category:{province} federal electoral districts"
        previous_name = f"Category:Former federal electoral districts of {province}"
        current_page = wiki.page(current_name)
        previous_page = wiki.page(previous_name)

        if current_page.exists():
            province_pages.update(current_page.categorymembers)
        if previous_page.exists():
            province_pages.update(previous_page.categorymembers)

        for page_name, page in province_pages.items():
            if any(s in page_name for s in STRINGS_TO_IGNORE):
                continue
            for suffix in SUFFIXES_TO_REMOVE:
                page_name = page_name.removesuffix(suffix.format(province=province))

            riding_pages.setdefault(province, {})
            riding_pages[province][page_name] = {
                "summary": page.summary.split("\n"),
                "url": page.fullurl
            }
            print(f"Getting summary for {page_name}, {province}")

    with open(RIDING_SUMMARY_FILE, "w") as f:
        json.dump(riding_pages, f, indent=4)
