## Macro functions.

# All versions use a YAML reference so they only have to be defined once,
# just grep for this reference and print it out.
config_reference = $(shell cat docker-compose.yml | grep '\&$(1)' | awk '{ print $$3 }' | tr -d "'")
config_release = $(call config_reference,$(1)_release)
config_version = $(call config_reference,$(1)_version)

# Variants for getting RPM file names.
RPMBUILD_DIST := $(call config_reference,rpmbuild_dist)
rpm_file = RPMS/$(2)/$(1)-$(call config_version,$(1))$(RPMBUILD_DIST).$(2).rpm

# Gets the RPM package name from the filename.
rpm_package = $(shell echo $(1) | awk '{ split($$0, a, "-"); l = length(a); pkg = a[1]; for (i=2; i<l-1; ++i) pkg = pkg "-" a[i]; print pkg }')
rpmbuild_image = $(call config_reference,$(call rpm_package,$(1))_image)
rpmbuild_version = $(shell echo $(call config_version,$(call rpm_package,$(1))) | awk -F- '{ print $$1 }')
rpmbuild_release = $(shell echo $(call config_version,$(call rpm_package,$(1))) | awk -F- '{ print $$2 }')


## Variables
DOCKER ?= docker
DOCKER_VERSION := $(shell $(DOCKER) --version 2>/dev/null)
DOCKER_COMPOSE ?= docker-compose
DOCKER_COMPOSE_VERSION := $(shell $(DOCKER_COMPOSE) --version 2>/dev/null)
POSTGRES_DOTLESS := $(shell echo $(call config_version,postgres) | tr -d '.')
RPMBUILD_CHANNEL := $(call config_reference,rpmbuild_channel)
RPMBUILD_UID := $(shell id -u)
RPMBUILD_GID := $(shell id -g)

# RPM files at desired versions.
OSMOSIS_RPM := $(call rpm_file,osmosis,noarch)
SBT_RPM := $(call rpm_file,sbt,noarch)
SQLITE_RPM := $(call rpm_file,sqlite,x86_64)


## General targets
all:
ifndef DOCKER_VERSION
    $(error "command docker is not available, please install Docker")
endif
ifndef DOCKER_COMPOSE_VERSION
    $(error "command docker-compose is not available, please install Docker")
endif

.PHONY: \
	all \
	distclean \
	rpmbuild \
	rpmbuild-generic \
	rpmbuild-sqlite \
	osmosis \
	sbt \
	sqlite \

.env: SPECS/*.spec
	echo COMPOSE_PROJECT_NAME=deps-$(RPMBUILD_CHANNEL) > .env
	echo RPMBUILD_GID=$(RPMBUILD_GID) >> .env
	echo RPMBUILD_UID=$(RPMBUILD_UID) >> .env
	echo SQLITE_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/sqlite.spec) >> .env

distclean: .env
	$(DOCKER_COMPOSE) down --volumes --rmi all
	rm -fr .env RPMS/noarch RPMS/x86_64 SOURCES/*.asc SOURCES/*.sha256 SOURCES/*.tgz SOURCES/*.tar.gz SOURCES/*.tar.xz SOURCES/*.zip


## Container targets

# Build containers.
rpmbuild: .env
	$(DOCKER_COMPOSE) up -d rpmbuild

rpmbuild-generic: .env
	$(DOCKER_COMPOSE) up -d rpmbuild-generic

rpmbuild-sqlite: .env
	$(DOCKER_COMPOSE) up -d rpmbuild-sqlite


## RPM targets

osmosis: rpmbuild-generic $(OSMOSIS_RPM)
sbt: rpmbuild-generic $(SBT_RPM)
sqlite: rpmbuild-sqlite $(SQLITE_RPM)


## Build patterns

# Runs container with docker-compose to build rpm.
RPMS/x86_64/%.rpm RPMS/noarch/%.rpm:
	$(DOCKER_COMPOSE) exec -T $(call rpmbuild_image,$*) rpmbuild \
	--define "rpmbuild_version $(call rpmbuild_version,$*)" \
	--define "rpmbuild_release $(call rpmbuild_release,$*)" \
	-bb SPECS/$(call rpm_package,$*).spec
