#!/bin/bash
set -euo pipefail

REPO="${1:-}"
REPODATA="${REPO}/repodata"

if [ -z "${REPO}" ]; then
    echo 'repo-update.sh: must provide a repository directory argument.'
    exit 1
fi

if [ ! -d "${REPO}" ] ; then
    mkdir -p "${REPO}"
fi

# Recreate the repository database with `createrepo`.
rm -r "${REPO}/repodata"
createrepo --database --xz "${REPO}"
