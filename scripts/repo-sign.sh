#!/bin/bash
set -euo pipefail

REPO="${1:-}"
if [ ! -d "${REPO}" ]; then
    echo 'repo-sign.sh: must provide a repository directory argument.'
    exit 1
fi

# Sign the repository metadata file.
gpg --detach-sign --armor --digest-algo sha512 "${REPO}/repodata/repomd.xml"
