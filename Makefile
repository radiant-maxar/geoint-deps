## Macro functions.

# All versions use a YAML reference so they only have to be defined once,
# just grep for this reference and print it out.
rpmbuild_util = $(shell ./scripts/rpmbuild_util.py docker-compose.yml $(1) $(2))
config_release = $(call rpmbuild_util,$(1),--release)
config_version = $(call rpmbuild_util,$(1),--version)

# Variants for getting RPM file names.
RPMBUILD_DIST := $(call rpmbuild_util,dist,--variable)
rpm_file = $(call rpmbuild_util,$(1),--filename)

# Gets the RPM package name from the filename.
rpm_package = $(shell ./scripts/rpm_package.py $(1))
rpmbuild_image = $(call rpmbuild_util,$(call rpm_package,$(1)),--image)
rpmbuild_release = $(call config_release,$(call rpm_package,$(1)))
rpmbuild_version = $(call config_version,$(call rpm_package,$(1)))

## Variables
DOCKER ?= docker
DOCKER_VERSION := $(shell $(DOCKER) --version 2>/dev/null)
DOCKER_COMPOSE ?= docker-compose
DOCKER_COMPOSE_VERSION := $(shell $(DOCKER_COMPOSE) --version 2>/dev/null)
POSTGRES_DOTLESS := $(shell echo $(call rpmbuild_util,postgres_version,--variable) | tr -d '.')
RPMBUILD_CHANNEL := $(call rpmbuild_util,channel_name,--variable)
RPMBUILD_UID := $(shell id -u)
RPMBUILD_GID := $(shell id -g)

# RPM files at desired versions.
CGAL_RPM := $(call rpm_file,CGAL)
FILEGDBAPI_RPM := $(call rpm_file,FileGDBAPI)
GDAL_RPM := $(call rpm_file,gdal)
GEOS_RPM := $(call rpm_file,geos)
GPSBABEL_RPM := $(call rpm_file,gpsbabel)
LIBGEOTIFF_RPM := $(call rpm_file,libgeotiff)
LIBKML_RPM := $(call rpm_file,libkml)
LIBOSMIUM_RPM := $(call rpm_file,libosmium)
MAPNIK_RPM := $(call rpm_file,mapnik)
OSMIUM_TOOL_RPM := $(call rpm_file,osmium-tool)
OSMOSIS_RPM := $(call rpm_file,osmosis)
PASSENGER_RPM := $(call rpm_file,passenger)
POSTGIS_RPM := $(call rpm_file,postgis)
PROJ_RPM := $(call rpm_file,proj)
PROJ6_RPM := $(call rpm_file,proj6)
PROTOBUF_RPM := $(call rpm_file,protobuf)
PROTOBUF_C_RPM := $(call rpm_file,protobuf-c)
PROTOZERO_RPM := $(call rpm_file,protozero)
RACK_RPM := $(call rpm_file,rubygem-rack)
RUBY_RPM := $(call rpm_file,ruby)
SBT_RPM := $(call rpm_file,sbt,noarch)
SFCGAL_RPM := $(call rpm_file,SFCGAL)
SQLITE_RPM := $(call rpm_file,sqlite)

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
	rpmbuild-passenger \
	rpmbuild-postgis \
	rpmbuild-proj \
	rpmbuild-protobuf \
	rpmbuild-protobuf-c \
	rpmbuild-protozero \
	rpmbuild-rack \
	rpmbuild-ruby \
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
	passenger \
	postgis \
	protobuf \
	protobuf-c \
	proj \
	proj6 \
	protozero \
	rack \
	ruby \
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
	echo RPMBUILD_MAPNIK_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/mapnik.spec) >> .env
	echo RPMBUILD_OSMIUM_TOOL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osmium-tool.spec) >> .env
	echo RPMBUILD_PASSENGER_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/passenger.spec) >> .env
	echo RPMBUILD_PROJ_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/proj.spec) >> .env
	echo RPMBUILD_POSTGIS_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/postgis.spec --define postgres_dotless=$(POSTGRES_DOTLESS)) >> .env
	echo RPMBUILD_PROTOBUF_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/protobuf.spec) >> .env
	echo RPMBUILD_PROTOBUF_C_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/protobuf-c.spec) >> .env
	echo RPMBUILD_PROTOZERO_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/protozero.spec) >> .env
	echo RPMBUILD_RACK_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/rubygem-rack.spec) >> .env
	echo RPMBUILD_RUBY_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/ruby.spec) >> .env
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

rpmbuild-mapnik: .env gdal postgis
	$(DOCKER_COMPOSE) up -d rpmbuild-mapnik

rpmbuild-osmium-tool: .env libosmium
	$(DOCKER_COMPOSE) up -d rpmbuild-osmium-tool

rpmbuild-passenger: .env rack
	$(DOCKER_COMPOSE) up -d rpmbuild-passenger

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

rpmbuild-rack: .env ruby
	$(DOCKER_COMPOSE) up -d rpmbuild-rack

rpmbuild-ruby: .env
	$(DOCKER_COMPOSE) up -d rpmbuild-ruby

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
mapnik: rpmbuild-mapnik $(MAPNIK_RPM)
osmium-tool: rpmbuild-osmium-tool $(OSMIUM_TOOL_RPM)
osmosis: rpmbuild-generic $(OSMOSIS_RPM)
passenger: rpmbuild-passenger $(PASSENGER_RPM)
postgis: rpmbuild-postgis $(POSTGIS_RPM)
proj: rpmbuild-proj $(PROJ_RPM)
proj6: rpmbuild-proj $(PROJ6_RPM)
protobuf: rpmbuild-protobuf $(PROTOBUF_RPM)
protobuf-c: rpmbuild-protobuf-c $(PROTOBUF_C_RPM)
protozero: rpmbuild-protozero $(PROTOZERO_RPM)
rack: rpmbuild-rack $(RACK_RPM)
ruby: rpmbuild-ruby $(RUBY_RPM)
sbt: rpmbuild-generic $(SBT_RPM)
sqlite: rpmbuild-sqlite $(SQLITE_RPM)

## Build patterns

# Runs container with docker-compose to build rpm.
RPMS/x86_64/%.rpm RPMS/noarch/%.rpm:
	$(DOCKER_COMPOSE) exec -T $(call rpmbuild_image,$*) \
	$(shell ./scripts/rpmbuild_util.py docker-compose.yml $(call rpm_package,$*))
