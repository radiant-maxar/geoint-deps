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

# Update (or create) the repository database with `createrepo`.
if [ ! -d "${REPODATA}" ]; then
    createrepo --database --unique-md-filenames "${REPO}"
else
    createrepo --update "${REPO}"
fi
