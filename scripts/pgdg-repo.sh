#!/bin/bash
set -euo pipefail

POSTGRES_VERSION="${1}"
PGDG_KEY="${PGDG_KEY:-/etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG}"
PGDG_REPO="${PGDG_REPO:-/etc/yum.repos.d/pgdg-${POSTGRES_VERSION}-centos.repo}"
PGDG_BASEURL="https://download.postgresql.org/pub/repos/yum"
if [ "${POSTGRES_VERSION}" -ge 16 ]; then
    PGDG_BASEURL="${PGDG_BASEURL}/testing"
fi

cat > "${PGDG_KEY}" <<EOF
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1.4.7 (GNU/Linux)

mQGiBEeD8koRBACC1VBRsUwGr9gxFFRho9kZpdRUjBJoPhkeOTvp9LzkdAQMFngr
BFi6N0ov1kCX7LLwBmDG+JPR7N+XcH9YR1coSHpLVg+JNy2kFDd4zAyWxJafjZ3a
9zFg9Yx+0va1BJ2t4zVcmKS4aOfbgQ5KwIOWUujalQW5Y+Fw39Gn86qjbwCg5dIo
tkM0l19h2sx50D027pV5aPsD/2c9pfcFTbMhB0CcKS836GH1qY+NCAdUwPs646ee
Ex/k9Uy4qMwhl3HuCGGGa+N6Plyon7V0TzZuRGp/1742dE8IO+I/KLy2L1d1Fxrn
XOTBZd8qe6nBwh12OMcKrsPBVBxn+iSkaG3ULsgOtx+HHLfa1/p22L5+GzGdxizr
peBuA/90cCp+lYcEwdYaRoFVR501yDOTmmzBc1DrsyWP79QMEGzMqa393G0VnqXt
L4pGmunq66Agw2EhPcIt3pDYiCmEt/obdVtSJH6BtmSDB/zYhbE8u3vLP3jfFDa9
KXxgtYj0NvuUVoRmxSKm8jtfmj1L7zoKNz3jl+Ba3L0WxIv4+bRBUG9zdGdyZVNR
TCBSUE0gQnVpbGRpbmcgUHJvamVjdCA8cGdzcWxycG1zLWhhY2tlcnNAcGdmb3Vu
ZHJ5Lm9yZz6IYAQTEQIAIAUCR4PySgIbIwYLCQgHAwIEFQIIAwQWAgMBAh4BAheA
AAoJEB8W0uFELfD4jnkAoMqd6ZwwsgYHZ3hP9vt+DJt1uDW7AKDbRwP8ESKFhwdJ
8m91RPBeJW/tMLkCDQRHg/JKEAgA64+ZXgcERPYfZYo4p+yMTJAAa9aqnE3U4Ni6
ZMB57GPuEy8NfbNya+HiftO8hoozmJdcI6XFyRBCDUVCdZ8SE+PJdOx2FFqZVIu6
dKnr8ykhgLpNNEFDG3boK9UfLj/5lYQ3Y550Iym1QKOgyrJYeAp6sZ+Nx2PavsP3
nMFCSD67BqAbcLCVQN7a2dAUXfEbfXJjPHXTbo1/kxtzE+KCRTLdXEbSEe3nHO04
K/EgTBjeBUOxnciH5RylJ2oGy/v4xr9ed7R1jJtshsDKMdWApwoLlCBJ63jg/4T/
z/OtXmu4AvmWaJxaTl7fPf2GqSqqb6jLCrQAH7AIhXr9V0zPZwADBQgAlpptNQHl
u7euIdIujFwwcxyQGfee6BG+3zaNSEHMVQMuc6bxuvYmgM9r7aki/b0YMfjJBk8v
OJ3Eh1vDH/woJi2iJ13vQ21ot+1JP3fMd6NPR8/qEeDnmVXu7QAtlkmSKI9Rdnjz
FFSUJrQPHnKsH4V4uvAM+njwYD+VFiwlBPTKNeL8cdBb4tPN2cdVJzoAp57wkZAN
VA2tKxNsTJKBi8wukaLWX8+yPHiWCNWItvyB4WCEp/rZKG4A868NM5sZQMAabpLd
l4fTiGu68OYgK9qUPZvhEAL2C1jPDVHPkLm+ZsD+90Pe66w9vB00cxXuHLzm8Pad
GaCXCY8h3xi6VIhJBBgRAgAJBQJHg/JKAhsMAAoJEB8W0uFELfD4K4cAoJ4yug8y
1U0cZEiF5W25HDzMTtaDAKCaM1m3Cbd+AZ0NGWNg/VvIX9MsPA==
=au6K
-----END PGP PUBLIC KEY BLOCK-----
EOF

cat > "${PGDG_REPO}" <<EOF
[pgdg${POSTGRES_VERSION}]
name=PostgreSQL ${POSTGRES_VERSION} \$releasever - \$basearch
baseurl=${PGDG_BASEURL}/${POSTGRES_VERSION}/redhat/rhel-\$releasever-\$basearch
enabled=1
exclude=CGAL* geos* gdal* ogdi* ogr* osm* postgis* proj* SFCGAL*
gpgcheck=1
gpgkey=file://${PGDG_KEY}
repo_gpgcheck=1

[pgdg${POSTGRES_VERSION}-source]
name=PostgreSQL ${POSTGRES_VERSION} \$releasever - \$basearch - Source
failovermethod=priority
baseurl=${PGDG_BASEURL}/srpms/${POSTGRES_VERSION}/redhat/rhel-\$releasever-\$basearch
enabled=0
gpgcheck=1
gpgkey=file://${PGDG_KEY}
repo_gpgcheck=1
EOF
