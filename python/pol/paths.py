from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

PYTHON_DIR = ROOT_DIR / "python"
WEB_DIR = ROOT_DIR / "web"
ARTIFACTS_DIR = ROOT_DIR / "artifacts"
SOURCES_DIR = ROOT_DIR / "sources"

PACKAGE_DIR = PYTHON_DIR / "pol"

WEB_ARTIFACTS_DIR = WEB_DIR / "src/lib/artifacts"

CACHE_DIR = ARTIFACTS_DIR / "cache"
