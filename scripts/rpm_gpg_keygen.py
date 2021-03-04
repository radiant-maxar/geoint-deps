#!/usr/bin/env python
import argparse
import os
import sys
from getpass import getpass

# python-gnupg
import gnupg

# Only use AES ciphers, omit CAST5.
DEFAULT_CIPHER_ALGO = "AES256"
DEFAULT_CIPHER_PREFERENCES = "AES256 AES192 AES"
DEFAULT_COMPRESSION_PREFERENCES = "ZLIB BZIP2 ZIP Uncompressed"
# SHA-2 only digest algorithms.
DEFAULT_DIGEST_ALGO = "SHA512"
DEFAULT_DIGEST_PREFERENCES = "SHA512 SHA384 SHA256"
DEFAULT_KEY_PREFERENCES = " ".join(
    [
        DEFAULT_DIGEST_PREFERENCES,
        DEFAULT_CIPHER_PREFERENCES,
        DEFAULT_COMPRESSION_PREFERENCES,
    ]
)
DEFAULT_KEY_LENGTH = 4096
DEFAULT_KEY_TYPE = "RSA"
DEFAULT_KEY_USAGE = "sign"


def main():
    # Get CLI arguments.
    parser = argparse.ArgumentParser(
        description="Generate GPG keys for signing RPMs and Yum repositories."
    )
    parser.add_argument(
        "-d",
        "--key-dest",
        dest="key_dest",
        help="Key destination.",
        metavar="DEST",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-n",
        "--key-name",
        dest="key_name",
        help="Key name.",
        metavar="NAME",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-e",
        "--key-email",
        dest="key_email",
        help="Key email address.",
        metavar="EMAIL",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-f",
        "--passphrase-file",
        dest="passphrase_file",
        metavar="PASSPHRASE_FILE",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "-l",
        "--key-length",
        default=DEFAULT_KEY_LENGTH,
        dest="key_length",
        help="Key length, defaults to: {}".format(DEFAULT_KEY_LENGTH),
        metavar="LENGTH",
        type=int,
    )
    parser.add_argument(
        "-t",
        "--key-type",
        default=DEFAULT_KEY_TYPE,
        dest="key_type",
        help="Key type, defaults to: {}".format(DEFAULT_KEY_TYPE),
        metavar="TYPE",
        type=str,
    )
    parser.add_argument(
        "-u",
        "--key-usage",
        dest="key_usage",
        help='Key usage, defaults to: "{}"'.format(DEFAULT_KEY_USAGE),
        default=DEFAULT_KEY_USAGE,
        metavar="USAGE",
        type=str,
    )
    args = parser.parse_args()

    # Create key destination.
    if not os.path.isdir(args.key_dest):
        os.makedirs(args.key_dest, mode=0o700)

    if args.passphrase_file:
        passphrase = args.passphrase_file.read()
    else:
        # Get and confirm the passphrase.
        passphrase = getpass("GPG Passphrase: ")
        passphrase_repeat = getpass("GPG Passphrase (again): ")
        if passphrase != passphrase_repeat:
            sys.stderr.write("GPG passhphrases do not match, aborting.\n")
            sys.exit(os.EX_IOERR)

    # Generate GPG key.
    rpm_gpg = gnupg.GPG(
        gnupghome=args.key_dest,
        options=[
            "--cert-digest-algo",
            DEFAULT_DIGEST_ALGO,
            "--cipher-algo",
            DEFAULT_CIPHER_ALGO,
            "--digest-algo",
            DEFAULT_DIGEST_ALGO,
            "--personal-cipher-preferences",
            DEFAULT_CIPHER_PREFERENCES,
            "--personal-digest-preferences",
            DEFAULT_DIGEST_PREFERENCES,
            "--s2k-cipher-algo",
            DEFAULT_CIPHER_ALGO,
            "--s2k-digest-algo",
            DEFAULT_DIGEST_ALGO,
            "--s2k-mode",
            "3",
            "--s2k-count",
            "65011712",
        ],
        verbose=True,
    )
    input_data = rpm_gpg.gen_key_input(
        key_length=args.key_length,
        key_type=args.key_type,
        key_usage=args.key_usage,
        name_email=args.key_email,
        name_real=args.key_name,
        passphrase=passphrase,
        preferences=DEFAULT_KEY_PREFERENCES,
    )
    rpm_gpg.gen_key(input_data)

    # Create default configuration file.
    gpg_conf = os.path.join(args.key_dest, "gpg.conf")
    with open(gpg_conf, "w") as gpg_fh:
        gpg_fh.write(
            "\n".join(
                [
                    "# behavior",
                    "no-comments",
                    "export-options export-minimal",
                    "no-emit-version",
                    "keyid-format 0xlong",
                    "with-fingerprint",
                    "list-options show-uid-validity",
                    "verify-options show-uid-validity",
                    "use-agent",
                    "",
                    "# algorithms and ciphers",
                    "cipher-algo %s" % DEFAULT_CIPHER_ALGO,
                    "cert-digest-algo %s" % DEFAULT_DIGEST_ALGO,
                    "digest-algo %s" % DEFAULT_DIGEST_ALGO,
                    "personal-cipher-preferences %s" % DEFAULT_CIPHER_PREFERENCES,
                    "personal-digest-preferences %s" % DEFAULT_DIGEST_PREFERENCES,
                    "default-preference-list %s" % DEFAULT_KEY_PREFERENCES,
                    "",
                ]
            )
        )
    os.chmod(gpg_conf, 0o600)

    sys.exit(os.EX_OK)


if __name__ == "__main__":
    main()
