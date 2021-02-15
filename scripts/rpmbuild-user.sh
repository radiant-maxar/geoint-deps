#!/bin/bash
set -euo pipefail

# Add unprivileged user for building RPMs.
groupadd -g "${RPMBUILD_GID}" "${RPMBUILD_GROUP}"
useradd -d "${RPMBUILD_HOME}" -m \
        -s "${RPMBUILD_SHELL:-/bin/bash}" \
        -u "${RPMBUILD_UID}" \
        -g "${RPMBUILD_GID}" \
        "${RPMBUILD_USER}"

# Git configuration.
cat > "${RPMBUILD_HOME}/.gitconfig" <<EOF
[url "https://"]
        insteadOf = git://
EOF

# RPM macros.
cat > "${RPMBUILD_HOME}/.rpmmacros" <<EOF
%_gpg_digest_algo ${RPMBUILD_GPG_DIGEST_ALGO:-sha512}
%_gpg_name ${RPMBUILD_GPG_NAME}
%_gpg_path ${RPMBUILD_GPG_PATH:-${RPMBUILD_HOME}/.gnupg}
%_hardened_build 1
%_topdir ${RPMBUILD_HOME}
%debug_package %{nil}
%dist ${RPMBUILD_DIST}
EOF

# Ensure proper permissions.
chown "${RPMBUILD_USER}:${RPMBUILD_GROUP}" \
      "${RPMBUILD_HOME}/.gitconfig" \
      "${RPMBUILD_HOME}/.rpmmacros"
chmod 0755 "${RPMBUILD_HOME}"
