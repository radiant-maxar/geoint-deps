#!/usr/bin/env bash
set -euo pipefail

RPMS_ZIP_FILE=${1:-"RPMS.zip"}
RPMS_ZIP_FILE_NAME=$(basename "${RPMS_ZIP_FILE}")

if [ ! -f "${RPMS_ZIP_FILE}" ]; then
  printf "ERROR: The zip file '%s' does not exist.\n" "${RPMS_ZIP_FILE}" 1>&2
  exit
fi

AWS_PROFILE=${AWS_PROFILE:-"geoint-deps"}
AWS_S3_BUCKET=${AWS_S3_BUCKET:-"geoint-deps"}
EL_VERSION=${EL_VERSION:-el7}

GIT_ROOT_DIR=$(git rev-parse --show-toplevel)
REPO_PREFIX="${EL_VERSION}/stable"

AWS_S3_REPO_URL="s3://${AWS_S3_BUCKET}/${REPO_PREFIX}"
COMPOSE_FILE="${GIT_ROOT_DIR}/docker-compose.${EL_VERSION}.yml"
EXTRACTED_RPMS_PATH="/tmp/${RPMS_ZIP_FILE_NAME}/RPMS"
LOCAL_REPO_PATH="/tmp/${RPMS_ZIP_FILE_NAME}/${REPO_PREFIX}"

AWS_SYNC_CMD="aws --profile=${AWS_PROFILE} s3 sync"
DOCKER_RUN_CMD="docker-compose run \
                --rm \
                --volume ${HOME}/.gnupg-geoint:/rpmbuild/.gnupg:rw \
                --volume ${EXTRACTED_RPMS_PATH}:/rpmbuild/EXTRACTED_RPMS:rw \
                --volume ${LOCAL_REPO_PATH}:/rpmbuild/${REPO_PREFIX}:rw \
                --volume ${GIT_ROOT_DIR}/scripts:/rpmbuild/scripts:ro \
                rpmbuild-generic"


# Ensure we are in the git repository's top-level directory
cd "${GIT_ROOT_DIR}"

# Ensure the .env file does not exist
rm .env

# Build the rpmbuild-generic image
make --file "Makefile.${EL_VERSION}" rpmbuild-generic

# Ensure extracted RPMs directory is empty
rm -rf "${EXTRACTED_RPMS_PATH}"

# Create extracted RPMs directory & local repo directory (if needed)
mkdir --parents "${EXTRACTED_RPMS_PATH}" "${LOCAL_REPO_PATH}"

# Extract RPMS_ZIP_FILE to EXTRACTED_RPMS_PATH
unzip "${RPMS_ZIP_FILE}" -d "${EXTRACTED_RPMS_PATH}"

# Sync the S3 repo to the local repo copy
${AWS_SYNC_CMD} --delete \
  "${AWS_S3_REPO_URL}"/ "${LOCAL_REPO_PATH}"/

# Export COMPOSE_FILE variable
export COMPOSE_FILE

# Sign the extracted RPMs
${DOCKER_RUN_CMD} \
  bash -c "rpm --addsign EXTRACTED_RPMS/*/*.rpm"
# Sync only the new (based on filename) extracted RPMs into the local repo copy
${DOCKER_RUN_CMD} \
  bash -c "rsync --archive --ignore-existing --verbose EXTRACTED_RPMS/*/*.rpm ${REPO_PREFIX}"
# Update the local repo copy
${DOCKER_RUN_CMD} \
  bash -c "./scripts/repo-update.sh ${REPO_PREFIX}"
# Sign the local repo copy
${DOCKER_RUN_CMD} \
  bash -c "./scripts/repo-sign.sh ${REPO_PREFIX}"

# Sync the local repo copy to the S3 repo (dry run)
${AWS_SYNC_CMD} --delete --dryrun \
  "${LOCAL_REPO_PATH}"/ "${AWS_S3_REPO_URL}"/

echo "-------------------------"
echo "Execute the following command if the dryrun output above appears correct:"
echo "${AWS_SYNC_CMD} --delete ${LOCAL_REPO_PATH}/ ${AWS_S3_REPO_URL}/"
