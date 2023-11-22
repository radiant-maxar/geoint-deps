#!/usr/bin/env python3
import argparse
import itertools
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
        action="append",
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
            build_defines = dict(
                define.split("=")
                for define in itertools.chain.from_iterable(args.defines)
            )
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(2)
    build_requirements = []

    for line in args.spec_file:
        if line.startswith("BuildRequires:"):
            # Apply define macros on entire line first.
            for define_macro, define_value in build_defines.items():
                line = line.replace("%%{%s}" % define_macro, define_value)

            # Parse build requirement.
            build_splits = line.split("BuildRequires:")[1].split()
            build_req = build_splits[0]
            if len(build_splits) >= 3 and build_splits[1] == "=":
                build_version = build_splits[2]
                build_requirements.append(f"{build_req}-{build_version}")
            else:
                build_requirements.append(build_req)

    if args.json:
        output = json.dumps(build_requirements)
    else:
        output = " ".join(build_requirements)
    sys.stdout.write(output + "\n")


if __name__ == "__main__":
    main()
