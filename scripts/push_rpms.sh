#!/usr/bin/env bash
set -eux
GIT_ROOT_DIR=$(git rev-parse --show-toplevel)

RPM_PREFIX=${1:-"gdal"}
REPO_PREFIX=${REPO_PREFIX:-"el7/testing"}

AWS_PROFILE=${AWS_PROFILE:-"geoint-deps"}
AWS_S3_BUCKET=${AWS_S3_BUCKET:-"geoint-deps"}
AWS_S3_REPO_URL="s3://${AWS_S3_BUCKET}/${REPO_PREFIX}"
LOCAL_REPO_PATH="${GIT_ROOT_DIR}/${REPO_PREFIX}"

AWS_SYNC_CMD="aws --profile=${AWS_PROFILE} s3 sync"

DOCKER_RUN_CMD="docker-compose run \
                --rm \
                --volume ${HOME}/.gnupg-geoint:/rpmbuild/.gnupg:rw \
                --volume ${GIT_ROOT_DIR}/RPMS:/rpmbuild/RPMS:rw \
                --volume ${GIT_ROOT_DIR}/el7:/rpmbuild/el7:rw \
                --volume ${GIT_ROOT_DIR}/scripts:/rpmbuild/scripts:ro \
                rpmbuild-generic"


# Sync the S3 repo to the local repo copy
${AWS_SYNC_CMD} --delete \
  "${AWS_S3_REPO_URL}"/ "${LOCAL_REPO_PATH}"/

# Sign the local RPMs
${DOCKER_RUN_CMD} \
  bash -c "ls RPMS/{noarch,x86_64}/${RPM_PREFIX}-*.rpm | xargs rpm --addsign"
# Copy the local RPMs into the local repo copy
${DOCKER_RUN_CMD} \
  bash -c "ls RPMS/{noarch,x86_64}/${RPM_PREFIX}-*.rpm | xargs --replace cp --verbose {} ${REPO_PREFIX}"
# Update the local repo copy
${DOCKER_RUN_CMD} \
  bash -c "./scripts/repo-update.sh ${REPO_PREFIX}"
# Sign the local repo copy
${DOCKER_RUN_CMD} \
  bash -c "./scripts/repo-sign.sh ${REPO_PREFIX}"

# Stop printing commands
set +x

# Sync the local repo copy to the S3 repo (dry run)
${AWS_SYNC_CMD} --delete --dryrun \
  "${LOCAL_REPO_PATH}"/ "${AWS_S3_REPO_URL}"/

echo "Execute the following command if the dryrun output above appears correct:"
echo "${AWS_SYNC_CMD} --delete ${LOCAL_REPO_PATH}/ ${AWS_S3_REPO_URL}/"
