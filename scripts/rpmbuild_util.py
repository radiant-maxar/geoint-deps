#!/usr/bin/env python3
import argparse
import subprocess
import sys
import yaml


def main():
    parser = argparse.ArgumentParser(
        description="rpmbuild utility"
    )
    parser.add_argument(
        "config_file",
        help="YAML file with rpmbuild configuration.",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "rpm",
        help="RPM name or variable to query.",
        type=str,
    )
    parser.add_argument(
        "--config-key",
        default="x-rpmbuild",
        help="Key in YAML file with rpmbuild configuration.",
        type=str,
    )
    parser.add_argument(
        "-f",
        "--filename",
        action="store_true",
        default=False,
        help="Output RPM filename.",
    )
    parser.add_argument(
        "-i",
        "--image",
        action="store_true",
        default=False,
        help="Output RPM build image.",
    )
    parser.add_argument(
        "-r",
        "--release",
        action="store_true",
        default=False,
        help="Output RPM release.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="Output RPM version.",
    )
    parser.add_argument(
        "--variable",
        action="store_true",
        default=False,
        help="Output RPM version.",
    )
    args = parser.parse_args()

    config_data = yaml.load(
        args.config_file, Loader=yaml.SafeLoader
    ).get(args.config_key, {"rpms": {}})
    if args.variable:
        output = config_data[args.rpm]
        sys.stdout.write(output + "\n")
        sys.exit(0)
    elif not args.rpm in config_data["rpms"]:
        alias = None
        for r_key, r_data in config_data["rpms"].items():
            if r_data.get("name", None) == args.rpm:
                alias = r_key
        if alias:
            args.rpm = alias
        else:
            sys.stderr.write("No RPM data found for {}.\n".format(args.rpm))
            sys.exit(1)

    rpm_data = config_data["rpms"][args.rpm]
    rpm_dist = config_data["dist"]
    rpm_arch = rpm_data.get("arch", "x86_64")
    rpm_full_version = rpm_data["version"]
    rpm_version, rpm_release = rpm_full_version.split("-")
    rpm_image = rpm_data["image"]
    rpm_name = rpm_data.get("name", args.rpm)

    if args.filename:
        output = "RPMS/{arch}/{name}-{version}-{release}{dist}.{arch}.rpm".format(
            arch=rpm_arch,
            dist=rpm_dist,
            name=rpm_name,
            release=rpm_release,
            version=rpm_version
        )
    elif args.image:
        output = rpm_image
    elif args.version:
        output = rpm_version
    elif args.release:
        output = rpm_release
    else:
        defines = rpm_data.get("defines", {})
        defines.update({
            "rpmbuild_version": rpm_version,
            "rpmbuild_release": rpm_release,
        })
        undefines = rpm_data.get("undefines", [])
        with_ = rpm_data.get("with", [])
        without = rpm_data.get("without", [])

        rpmbuild_cmd = ["rpmbuild"]
        for define_name, define_value in defines.items():
            rpmbuild_cmd.append("--define")
            rpmbuild_cmd.append("'{} {}'".format(define_name, define_value))
        for undefine in undefines:
            rpmbuild_cmd.append("--undefine")
            rpmbuild_cmd.append(undefine)
        for w in with_:
            rpmbuild_cmd.append("--with")
            rpmbuild_cmd.append(w)
        for w in without:
            rpmbuild_cmd.append("--without")
            rpmbuild_cmd.append(w)

        if rpm_data.get("nocheck", False):
            rpmbuild_cmd.append("--nocheck")

        rpmbuild_cmd.append(rpm_data.get("build_type", "-bb"))
        rpmbuild_cmd.append(rpm_data.get(
            "spec_file", "SPECS/{}.spec".format(args.rpm)
        ))
        output = " ".join(rpmbuild_cmd)

    if output:
        sys.stdout.write(output + "\n")


if __name__ == "__main__":
    main()
