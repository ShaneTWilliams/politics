import wikipediaapi
import json
from pprint import pprint

USER_AGENT = "Shane Williams' Python bot (shanethomaswilliams@gmail.com)"
ELECTION_DATA_PATH = "web/src/lib/artifacts/election.json"
RIDING_DATA_PATH = "web/src/lib/artifacts/riding.json"

with open(ELECTION_DATA_PATH, "r") as f:
    election_data = json.load(f)

with open(RIDING_DATA_PATH, "r") as f:
    riding_data = json.load(f)

wiki = wikipediaapi.Wikipedia(USER_AGENT, "en")

# summaries = {}
# for election in list(election_data.values()):
#     if election["type"] != "GENERAL":
#         continue
# 
#     year = election["date"]["year"]
#     page = wiki.page(f"{year} Canadian federal election")
#     if not page.exists():
#         print(f"Page for {year} does not exist")
#         continue
# 
#     summaries[year] = page.summary.split("\n")
# 
# with open("wiki.json", "w") as f:
#     json.dump(summaries, f, indent=4)

def print_categorymembers(categorymembers, level=0, max_level=1):
    for c in categorymembers.values():
        print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)

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
        print(province, page_name)

with open("sources/riding_summaries.json", "w") as f:
    json.dump(riding_pages, f, indent=4)
