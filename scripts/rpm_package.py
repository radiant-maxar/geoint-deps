#!/usr/bin/env python3
import argparse
import os
import re
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "rpm_file",
        help="RPM file name to derive the package name from.",
        type=str
    )
    args = parser.parse_args()

    version_match = re.compile('^\d+\.').match
    package_bits = []
    for package_bit in os.path.basename(args.rpm_file).split('-'):
        if version_match(package_bit):
            break
        else:
            package_bits.append(package_bit)
    package_name = "-".join(package_bits)
    sys.stdout.write(package_name)


if __name__ == "__main__":
    main()
