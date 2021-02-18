#!/bin/bash
set -euo pipefail
POSTGRES_VERSION="${1}"
POSTGRES_DOTLESS="$(echo "${POSTGRES_VERSION}" | awk '{ gsub(/\./, ""); print substr($0, 1, 2) }')"
POSTGRES_MAJOR_VERSION="$(echo "${POSTGRES_VERSION}" | awk -F. '{ if ($1 >= 10) print $1; else print $0 }')"

# Install PostgreSQL server and its contrib package.
yum -q -y install epel-release
yum -q -y install \
    "postgresql${POSTGRES_DOTLESS}" \
    "postgresql${POSTGRES_DOTLESS}-contrib" \
    "postgresql${POSTGRES_DOTLESS}-server"

# Install alternatives for common PostgreSQL programs.
alternatives --install /usr/bin/createdb pgsql-createdb \
             "/usr/pgsql-${POSTGRES_MAJOR_VERSION}/bin/createdb" 500
alternatives --install /usr/bin/createuser pgsql-createuser \
             "/usr/pgsql-${POSTGRES_MAJOR_VERSION}/bin/createuser" 500
alternatives --install /usr/bin/initdb pgsql-initdb \
             "/usr/pgsql-${POSTGRES_MAJOR_VERSION}/bin/initdb" 500
alternatives --install /usr/bin/pg_config pgsql-pg_config \
             "/usr/pgsql-${POSTGRES_MAJOR_VERSION}/bin/pg_config" 500
alternatives --install /usr/bin/pg_ctl pgsql-pg_ctl \
             "/usr/pgsql-${POSTGRES_MAJOR_VERSION}/bin/pg_ctl" 500
alternatives --install /usr/bin/postgres pgsql-postgres \
             "/usr/pgsql-${POSTGRES_MAJOR_VERSION}/bin/postgres" 500
