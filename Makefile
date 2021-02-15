# Default commands for Docker and Vagrant.
DOCKER ?= docker
VAGRANT ?= vagrant

## Macro functions.

# All versions use a YAML reference so they only have to be defined once,
# just grep for this reference and print it out.
config_reference = $(shell cat docker-compose.yml | grep '\&$(1)' | awk '{ print $$3 }' | tr -d "'")
config_release = $(call config_reference,$(1)_release)
config_version = $(call config_reference,$(1)_version)

# Where Vagrant puts the Docker container id after it's been created.
container_id = .vagrant/machines/$(1)/docker/id

# Follows the docker logs for the given container.
docker_logs = $(DOCKER) logs --follow $$(cat $(call container_id,$(1)))

# Variants for getting RPM file names.
RPMBUILD_DIST := $(call config_reference,rpmbuild_dist)
rpm_file = RPMS/$(2)/$(1)-$(call config_version,$(1))$(RPMBUILD_DIST).$(2).rpm
rpm_file2 = RPMS/$(3)/$(1)-$(call config_version,$(2))$(RPMBUILD_DIST).$(3).rpm
rpm_file3 = RPMS/$(2)/$(1)-$(call config_version,$(1))-$(call config_release,$(1))$(RPMBUILD_DIST).$(2).rpm
rpm_file4 = RPMS/$(3)/$(1)-$(call config_version,$(2))$(4).$(3).rpm

# Gets the RPM package name from the filename.
rpm_package = $(shell echo $(1) | awk '{ split($$0, a, "-"); l = length(a); pkg = a[1]; for (i=2; i<l-1; ++i) pkg = pkg "-" a[i]; print pkg }')
PG_DOTLESS := $(shell echo $(call config_version,pg) | tr -d '.')

# RPM files at desired versions.
OSMOSIS_RPM := $(call rpm_file,osmosis,noarch)
SBT_RPM := $(call rpm_file,sbt,noarch)


## General targets

BASE_CONTAINERS := \
	rpmbuild \
	rpmbuild-generic

.PHONY: \
	all \
	osmosis \
	sbt \
	$(BASE_CONTAINERS)

clean:
	$(VAGRANT) destroy -f --no-parallel || true
	rm -fr RPMS/noarch RPMS/x86_64 SOURCES/*.tar.gz SOURCES/*.tar.xz SOURCES/*.zip


## Container targets

# Base containers
rpmbuild: .vagrant/machines/rpmbuild/docker/id

rpmbuild-generic: \
	rpmbuild \
	.vagrant/machines/rpmbuild-generic/docker/id


## RPM targets

osmosis: rpmbuild-generic $(OSMOSIS_RPM)
sbt: rpmbuild-generic $(SBT_RPM)


## Build patterns

# Builds a container with Vagrant.
.vagrant/machines/%/docker/id:
	$(VAGRANT) up $*

# Runs container and follow logs until it completes.
RPMS/x86_64/%.rpm RPMS/noarch/%.rpm:
	$(VAGRANT) up $(call rpm_package,$*)
	$(call docker_logs,$(call rpm_package,$*))
