## Macro functions.

# All versions use a YAML reference so they only have to be defined once,
# just grep for this reference and print it out.
config_reference = $(shell cat docker-compose.yml | grep '\&$(1)' | awk '{ print $$3 }' | tr -d "'\"")
config_release = $(call config_reference,$(1)_release)
config_version = $(call config_reference,$(1)_version)

# Variants for getting RPM file names.
RPMBUILD_DIST := $(call config_reference,rpmbuild_dist)
rpm_file = RPMS/$(2)/$(1)-$(call config_version,$(1))$(RPMBUILD_DIST).$(2).rpm
rpm_file2 = RPMS/$(3)/$(1)-$(call config_version,$(2))$(RPMBUILD_DIST).$(3).rpm

# Gets the RPM package name from the filename.
rpm_package = $(shell ./scripts/rpm_package.py $(1))
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
CGAL_RPM := $(call rpm_file,CGAL,x86_64)
FILEGDBAPI_RPM := $(call rpm_file,FileGDBAPI,x86_64)
GDAL_RPM := $(call rpm_file,gdal,x86_64)
GEOS_RPM := $(call rpm_file,geos,x86_64)
GPSBABEL_RPM := $(call rpm_file,gpsbabel,x86_64)
LIBGEOTIFF_RPM := $(call rpm_file,libgeotiff,x86_64)
LIBKML_RPM := $(call rpm_file,libkml,x86_64)
LIBOSMIUM_RPM := $(call rpm_file2,libosmium-devel,libosmium,noarch)
OSMIUM_TOOL_RPM := $(call rpm_file,osmium-tool,x86_64)
OSMOSIS_RPM := $(call rpm_file,osmosis,noarch)
POSTGIS_RPM := $(call rpm_file,postgis,x86_64)
PROJ_RPM := $(call rpm_file,proj,x86_64)
PROJ6_RPM := $(call rpm_file2,proj,proj6,x86_64)
PROTOBUF_RPM := $(call rpm_file,protobuf,x86_64)
PROTOBUF_C_RPM := $(call rpm_file,protobuf-c,x86_64)
PROTOZERO_RPM := $(call rpm_file2,protozero-devel,protozero,noarch)
SBT_RPM := $(call rpm_file,sbt,noarch)
SFCGAL_RPM := $(call rpm_file,SFCGAL,x86_64)
SQLITE_RPM := $(call rpm_file,sqlite,x86_64)

# Build containers and RPMs.
RPMBUILD_CONTAINERS := \
	rpmbuild \
	rpmbuild-cgal \
	rpmbuild-generic \
	rpmbuild-gdal \
	rpmbuild-geos \
	rpmbuild-gpsbabel \
	rpmbuild-libgeotiff \
	rpmbuild-libkml \
	rpmbuild-libosmium \
	rpmbuild-osmium-tool \
	rpmbuild-postgis \
	rpmbuild-proj \
	rpmbuild-protobuf \
	rpmbuild-protobuf-c \
	rpmbuild-protozero \
	rpmbuild-sfcgal \
	rpmbuild-sqlite
RPMBUILD_RPMS := \
	CGAL \
	FileGDBAPI \
	SFCGAL \
	gdal \
	geos \
	gpsbabel \
	libgeotiff \
	libkml \
	libosmium \
	osmosis \
	osmium-tool \
	postgis \
	protobuf \
	protobuf-c \
	proj \
	proj6 \
	protozero \
	sbt \
	sqlite

## General targets

.PHONY: \
	all \
	distclean \
	$(RPMBUILD_CONTAINERS) \
	$(RPMBUILD_RPMS)

all:
ifndef DOCKER_VERSION
    $(error "command docker is not available, please install Docker")
endif
ifndef DOCKER_COMPOSE_VERSION
    $(error "command docker-compose is not available, please install Docker")
endif

distclean: .env
	$(DOCKER_COMPOSE) down --volumes --rmi all
	rm -fr .env RPMS/noarch RPMS/x86_64 SOURCES/*.asc SOURCES/*.sha256 SOURCES/*.tgz SOURCES/*.tar.gz SOURCES/*.tar.xz SOURCES/*.zip

# Environment file for docker-compose; required packages for build containers
# are provided here.
.env: SPECS/*.spec
	echo COMPOSE_PROJECT_NAME=deps-$(RPMBUILD_CHANNEL) > .env
	echo RPMBUILD_GID=$(RPMBUILD_GID) >> .env
	echo RPMBUILD_UID=$(RPMBUILD_UID) >> .env
	echo RPMBUILD_CGAL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/CGAL.spec) >> .env
	echo RPMBUILD_GDAL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/gdal.spec --define postgres_dotless=$(POSTGRES_DOTLESS)) >> .env
	echo RPMBUILD_GEOS_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/geos.spec) >> .env
	echo RPMBUILD_GPSBABEL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/gpsbabel.spec) >> .env
	echo RPMBUILD_LIBGEOTIFF_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/libgeotiff.spec) >> .env
	echo RPMBUILD_LIBKML_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/libkml.spec) >> .env
	echo RPMBUILD_LIBOSMIUM_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/libosmium.spec) >> .env
	echo RPMBUILD_OSMIUM_TOOL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osmium-tool.spec) >> .env
	echo RPMBUILD_PROJ_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/proj.spec) >> .env
	echo RPMBUILD_POSTGIS_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/postgis.spec --define postgres_dotless=$(POSTGRES_DOTLESS)) >> .env
	echo RPMBUILD_PROTOBUF_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/protobuf.spec) >> .env
	echo RPMBUILD_PROTOBUF_C_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/protobuf-c.spec) >> .env
	echo RPMBUILD_PROTOZERO_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/protozero.spec) >> .env
	echo RPMBUILD_SFCGAL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/SFCGAL.spec) >> .env
	echo RPMBUILD_SQLITE_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/sqlite.spec) >> .env

## Container targets

# Build containers.
rpmbuild: .env
	$(DOCKER_COMPOSE) up -d rpmbuild

rpmbuild-cgal: .env
	$(DOCKER_COMPOSE) up -d rpmbuild-cgal

rpmbuild-generic: .env
	$(DOCKER_COMPOSE) up -d rpmbuild-generic

rpmbuild-gdal: .env CGAL FileGDBAPI SFCGAL geos gpsbabel libgeotiff libkml proj sqlite
	$(DOCKER_COMPOSE) up -d rpmbuild-gdal

rpmbuild-geos: .env
	$(DOCKER_COMPOSE) up -d rpmbuild-geos

rpmbuild-gpsbabel: .env
	$(DOCKER_COMPOSE) up -d rpmbuild-gpsbabel

rpmbuild-libgeotiff: .env proj
	$(DOCKER_COMPOSE) up -d rpmbuild-libgeotiff

rpmbuild-libkml: .env
	$(DOCKER_COMPOSE) up -d rpmbuild-libkml

rpmbuild-libosmium: .env protozero
	$(DOCKER_COMPOSE) up -d rpmbuild-libosmium

rpmbuild-osmium-tool: .env libosmium
	$(DOCKER_COMPOSE) up -d rpmbuild-osmium-tool

rpmbuild-pgdg: .env
	$(DOCKER_COMPOSE) up -d rpmbuild-pgdg

rpmbuild-postgis: .env gdal protobuf-c
	$(DOCKER_COMPOSE) up -d rpmbuild-postgis

rpmbuild-proj: .env sqlite
	$(DOCKER_COMPOSE) up -d rpmbuild-proj

rpmbuild-protobuf: .env
	$(DOCKER_COMPOSE) up -d rpmbuild-protobuf

rpmbuild-protobuf-c: .env protobuf
	$(DOCKER_COMPOSE) up -d rpmbuild-protobuf-c

rpmbuild-protozero: .env
	$(DOCKER_COMPOSE) up -d rpmbuild-protozero

rpmbuild-sfcgal: .env $(CGAL_RPM)
	$(DOCKER_COMPOSE) up -d rpmbuild-sfcgal

rpmbuild-sqlite: .env
	$(DOCKER_COMPOSE) up -d rpmbuild-sqlite

## RPM targets

CGAL: rpmbuild-cgal $(CGAL_RPM)
FileGDBAPI: rpmbuild-generic $(FILEGDBAPI_RPM)
SFCGAL: rpmbuild-sfcgal $(SFCGAL_RPM)
gdal: rpmbuild-gdal $(GDAL_RPM)
geos: rpmbuild-geos $(GEOS_RPM)
gpsbabel: rpmbuild-gpsbabel $(GPSBABEL_RPM)
libgeotiff: rpmbuild-libgeotiff $(LIBGEOTIFF_RPM)
libkml: rpmbuild-libkml $(LIBKML_RPM)
libosmium: rpmbuild-libosmium $(LIBOSMIUM_RPM)
osmium-tool: rpmbuild-osmium-tool $(OSMIUM_TOOL_RPM)
osmosis: rpmbuild-generic $(OSMOSIS_RPM)
postgis: rpmbuild-postgis $(POSTGIS_RPM)
proj: rpmbuild-proj $(PROJ_RPM)
proj6: rpmbuild-proj $(PROJ6_RPM)
protobuf: rpmbuild-protobuf $(PROTOBUF_RPM)
protobuf-c: rpmbuild-protobuf-c $(PROTOBUF_C_RPM)
protozero: rpmbuild-protozero $(PROTOZERO_RPM)
sbt: rpmbuild-generic $(SBT_RPM)
sqlite: rpmbuild-sqlite $(SQLITE_RPM)

## Build patterns

# Special exception for PROJ 6 version; required by Tasking Manager 4;
# might be able to get rid of this if upgraded TM4 backend to pyproj==3.x.
RPMS/x86_64/proj-6%.rpm:
	$(DOCKER_COMPOSE) exec -T $(call rpmbuild_image,proj6) rpmbuild \
	--define "rpmbuild_version $(call rpmbuild_version,proj6)" \
	--define "rpmbuild_release $(call rpmbuild_release,proj6)" \
	-bb SPECS/proj6.spec

# `libosmium-devel` the package name instead of `libosmium`.
RPMS/noarch/libosmium-%.rpm:
	$(DOCKER_COMPOSE) exec -T $(call rpmbuild_image,libosmium) rpmbuild \
	--define "rpmbuild_version $(call rpmbuild_version,libosmium)" \
	--define "rpmbuild_release $(call rpmbuild_release,libosmium)" \
	-bb SPECS/libosmium.spec

# `protozero-devel` the package name instead of `protozero`.
RPMS/noarch/protozero-%.rpm:
	$(DOCKER_COMPOSE) exec -T $(call rpmbuild_image,protozero) rpmbuild \
	--define "rpmbuild_version $(call rpmbuild_version,protozero)" \
	--define "rpmbuild_release $(call rpmbuild_release,protozero)" \
	-bb SPECS/protozero.spec

# Runs container with docker-compose to build rpm.
RPMS/x86_64/%.rpm RPMS/noarch/%.rpm:
	$(DOCKER_COMPOSE) exec -T $(call rpmbuild_image,$*) rpmbuild \
	--define "rpmbuild_version $(call rpmbuild_version,$*)" \
	--define "rpmbuild_release $(call rpmbuild_release,$*)" \
	-bb SPECS/$(call rpm_package,$*).spec
