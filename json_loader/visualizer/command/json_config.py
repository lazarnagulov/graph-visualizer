import sys
import json
import os

from typing_extensions import List

PATH = os.path.join("", "json_loader", "config.json")
FIELDS = ['id-field', 'ref-prefix']

def config() -> None:
    argv: List[str] = sys.argv[1:]
    curr: int = 0
    argc: int = len(argv)

    if len(argv) < 1:
        print("[JSON_LOADER] please provide arguments")
        __print_config_usage()
        return

    while curr <= argc - 1:
        match argv[curr]:
            case 'init':
                with open(PATH, "w") as f:
                    f.write(json.dumps({"id-field": "@id", "ref-prefix" : "&"}, indent=4))
                    print(f"[JSON_LOADER] successfully created config file in { os.path.realpath(f.name) }")
                    curr += 1
            case _ if argv[curr].startswith('--'):
                cmd: str = argv[curr].lstrip('--')
                if cmd not in FIELDS:
                    print("[JSON_LOADER] invalid command")
                    __print_config_usage()
                    return
                if curr + 1 >= argc:
                    print(f"[JSON_LOADER] expected name after --{ cmd }")
                    return
                __update_value(cmd, argv[curr + 1])
                curr += 2
            case '--help' | '-h':
                __print_config_usage()
                curr += 1
            case _:
                print("[JSON_LOADER] invalid command")
                return

def __print_config_usage() -> None:
    print("""
            Json Loader Config:

              Usage:
                json_loader init                    - Initializes the JSON config file
                json_loader --id-field <id>         - Sets a new ID for the config (replace <id> with your desired value)
                json_loader --ref-prefix <prefix>   - Sets a new reference for the config (replace <prefix> with your desired value)
                json_loader --help | -h             - Shows this help page
            """)

def __update_value(key: str, value: str) -> None:
    if os.path.exists(PATH):
        with open(PATH, "r+") as f:
            config_data = json.load(f)
            config_data[key] = value
            f.seek(0)
            f.write(json.dumps(config_data, indent=4))
            f.truncate()
        print(f"[JSON_LOADER] successfully updated the {key} to '{value}' in {os.path.realpath(PATH)}")
    else:
        print(f"[JSON_LOADER] config file {PATH} does not exist. Initialize it first with `json_loader init`")
