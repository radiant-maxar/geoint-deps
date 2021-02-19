#!/usr/bin/env python3
import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "spec_file",
        help="RPM SPEC file to gather build requirements from.",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "--define",
        action="extend",
        dest="defines",
        nargs="+",
        help="RPM macro definitions to use.",
        type=str,
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        default=False,
        help="Output as JSON, default is plain text.",
    )
    args = parser.parse_args()

    build_defines = {}
    try:
        if args.defines:
            build_defines = dict(define.split("=") for define in args.defines)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(2)
    build_requirements = []

    for line in args.spec_file:
        if line.startswith("BuildRequires:"):
            build_req = line.split("BuildRequires:")[1].split()[0]
            for define_macro, define_value in build_defines.items():
                build_req = build_req.replace("%%{%s}" % define_macro, define_value)
            build_requirements.append(build_req)

    if args.json:
        output = json.dumps(build_requirements)
    else:
        output = " ".join(build_requirements)
    sys.stdout.write(output)


if __name__ == "__main__":
    main()
