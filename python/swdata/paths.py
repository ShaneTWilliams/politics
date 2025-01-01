from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

PYTHON_DIR = ROOT_DIR / "python"
WEB_DIR = ROOT_DIR / "web"
ARTIFACT_DIR = ROOT_DIR / "artifacts"
SOURCES_DIR = ROOT_DIR / "sources"

PYTHON_PACKAGE_DIR = PYTHON_DIR / "pol"

GEOMETRY_ARTIFACT_DIR = WEB_DIR / "static/geometry"
WEB_ARTIFACT_DIR = WEB_DIR / "src/lib/artifacts"

CACHE_DIR = ARTIFACT_DIR / "cache"
JSON_CACHE_DIR = CACHE_DIR / "json"
GEO_CACHE_DIR = CACHE_DIR / "geo"

GEOMETRY_DIR = SOURCES_DIR / "geometry/fedshapes_cbf_20221003"
ELECTION_SUMMARY_JSON = SOURCES_DIR / "election_summaries.json"
RIDING_SUMMARY_JSON = SOURCES_DIR / "riding_summaries.json"
