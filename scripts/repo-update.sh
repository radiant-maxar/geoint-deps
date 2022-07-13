#!/bin/bash
set -euo pipefail

source /etc/os-release
REPO="${1:-}"
REPODATA="${REPO}/repodata"

if [ -z "${REPO}" ]; then
    echo 'repo-update.sh: must provide a repository directory argument.'
    exit 1
fi

if [ ! -d "${REPO}" ] ; then
    mkdir -p "${REPO}"
fi

if [ "${VERSION_ID}" == "7" ]; then
    # Update (or create) the repository database with `createrepo`.
    if [ ! -d "${REPODATA}" ]; then
        createrepo --database --unique-md-filenames --deltas "${REPO}"
    else
        createrepo --update "${REPO}"
    fi
elif [ "${VERSION_ID}" == "9" ]; then
    # Recreate the repository database with `createrepo`.
    rm -fr "${REPODATA}"
    createrepo --database --xz "${REPO}"
fi
