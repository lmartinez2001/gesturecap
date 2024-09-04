import yaml

def parse_yml(to_parse: str) -> dict:
    with open(to_parse, 'r') as f:
        parsed: dict = yaml.safe_load(f)
    return parsed
