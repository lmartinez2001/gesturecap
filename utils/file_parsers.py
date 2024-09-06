import yaml

def parse_yml(to_parse: str) -> dict:
    """
    Parses a YAML file and returns its content as a dictionary


    Parameters:
    ---
    to_parse: str
        The path to the YAML file to be parsed


    Returns
    ---
    parsed: dict
        The content of the YAML file as a dictionary
    """
    with open(to_parse, 'r') as f:
        parsed: dict = yaml.safe_load(f)
    return parsed
