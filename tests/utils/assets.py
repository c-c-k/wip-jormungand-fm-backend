from pathlib import Path

ASSETS_ROOT = Path(__file__).parent.joinpath("assets").resolve()


class Assets:
    """Convenience class for getting Path objects to asset files."""
    ouraiports_countries_sample = ASSETS_ROOT.joinpath("ourairports/countries.csv")
    ouraiports_airports_sample = ASSETS_ROOT.joinpath("ourairports/airports.csv")
