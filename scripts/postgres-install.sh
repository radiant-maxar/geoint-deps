#!/bin/bash
set -euo pipefail
POSTGRES_VERSION="${1}"

# Install PostgreSQL server and its contrib package.
yum -q -y install epel-release
yum -q -y install \
    "postgresql${POSTGRES_VERSION}" \
    "postgresql${POSTGRES_VERSION}-contrib" \
    "postgresql${POSTGRES_VERSION}-server"

# Install alternatives for common PostgreSQL programs.
alternatives --install /usr/bin/createdb pgsql-createdb \
             "/usr/pgsql-${POSTGRES_VERSION}/bin/createdb" 500
alternatives --install /usr/bin/createuser pgsql-createuser \
             "/usr/pgsql-${POSTGRES_VERSION}/bin/createuser" 500
alternatives --install /usr/bin/initdb pgsql-initdb \
             "/usr/pgsql-${POSTGRES_VERSION}/bin/initdb" 500
alternatives --install /usr/bin/pg_config pgsql-pg_config \
             "/usr/pgsql-${POSTGRES_VERSION}/bin/pg_config" 500
alternatives --install /usr/bin/pg_ctl pgsql-pg_ctl \
             "/usr/pgsql-${POSTGRES_VERSION}/bin/pg_ctl" 500
alternatives --install /usr/bin/pg_isready pgsql-pg_isready \
             "/usr/pgsql-${POSTGRES_VERSION}/bin/pg_isready" 500
alternatives --install /usr/bin/postgres pgsql-postgres \
             "/usr/pgsql-${POSTGRES_VERSION}/bin/postgres" 500
