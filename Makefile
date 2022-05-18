## Conditional variables.
DOCKER ?= docker
DOCKER_COMPOSE ?= docker-compose
COMPOSE_FILE ?= docker-compose.yml

## Macro functions.

# The `rpmbuild_util.py` utility script is used to pull out configured versions,
# Docker build images, and other build variables.
rpmbuild_util = $(shell ./scripts/rpmbuild_util.py $(1) --config-file $(COMPOSE_FILE) $(2))
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
DOCKER_VERSION := $(shell $(DOCKER) --version 2>/dev/null)
DOCKER_COMPOSE_VERSION := $(shell $(DOCKER_COMPOSE) --version 2>/dev/null)
POSTGRES_DOTLESS := $(shell echo $(call rpmbuild_util,postgres_version,--variable) | tr -d '.')
RPMBUILD_CHANNEL := $(call rpmbuild_util,channel_name,--variable)
RPMBUILD_UID := $(shell id -u)
RPMBUILD_GID := $(shell id -g)

# RPM files at desired versions.
CGAL_RPM := $(call rpm_file,CGAL)
DUMB_INIT_RPM := $(call rpm_file,dumb-init)
FILEGDBAPI_RPM := $(call rpm_file,FileGDBAPI)
GDAL_RPM := $(call rpm_file,gdal)
GEOS_RPM := $(call rpm_file,geos)
GOOGLE_NOTO_RPM := $(call rpm_file,google-noto-fonts-extra)
GPSBABEL_RPM := $(call rpm_file,gpsbabel)
HANAZONO_RPM := $(call rpm_file,hanazono-fonts)
JOURNALD_CLOUDWATCH_LOGS_RPM := $(call rpm_file,journald-cloudwatch-logs)
LIBGEOTIFF_RPM := $(call rpm_file,libgeotiff)
LIBGTA_RPM := $(call rpm_file,libgta)
LIBKML_RPM := $(call rpm_file,libkml)
LIBOSMIUM_RPM := $(call rpm_file,libosmium)
MAPNIK_RPM := $(call rpm_file,mapnik)
MOD_TILE_RPM := $(call rpm_file,mod_tile)
OPENSTREETMAP_CARTO_RPM := $(call rpm_file,openstreetmap-carto)
OSMCTOOLS_RPM := $(call rpm_file,osmctools)
OSMDBT_RPM := $(call rpm_file,osmdbt)
OSMIUM_TOOL_RPM := $(call rpm_file,osmium-tool)
OSMOSIS_RPM := $(call rpm_file,osmosis)
OSM2PGSQL_RPM := $(call rpm_file,osm2pgsql)
PASSENGER_RPM := $(call rpm_file,passenger)
POSTGIS_RPM := $(call rpm_file,postgis)
PROJ_RPM := $(call rpm_file,proj)
PROTOZERO_RPM := $(call rpm_file,protozero)
PYOSMIUM_RPM := $(call rpm_file,python3-osmium)
PYTHON_MAPNIK_RPM := $(call rpm_file,python-mapnik)
RACK_RPM := $(call rpm_file,rubygem-rack)
RUBYGEM_LIBXML_RUBY_RPM := $(call rpm_file,rubygem-libxml-ruby)
SBT_RPM := $(call rpm_file,sbt,noarch)
SFCGAL_RPM := $(call rpm_file,SFCGAL)
SQLITE_PCRE_RPM := $(call rpm_file,sqlite-pcre)
TBB_RPM := $(call rpm_file,tbb)

# Build containers and RPMs.
RPMBUILD_CONTAINERS := \
	rpmbuild \
	rpmbuild-cgal \
	rpmbuild-fonts \
	rpmbuild-generic \
	rpmbuild-gdal \
	rpmbuild-gpsbabel \
	rpmbuild-journald-cloudwatch-logs \
	rpmbuild-libgeotiff \
	rpmbuild-libkml \
	rpmbuild-libosmium \
	rpmbuild-openstreetmap-carto \
	rpmbuild-osmctools \
	rpmbuild-osmdbt \
	rpmbuild-osmium-tool \
	rpmbuild-osm2pgsql \
	rpmbuild-passenger \
	rpmbuild-postgis \
	rpmbuild-proj \
	rpmbuild-protozero \
	rpmbuild-pyosmium \
	rpmbuild-rack \
	rpmbuild-rubygem-libxml-ruby \
	rpmbuild-sfcgal \
	rpmbuild-tbb
RPMBUILD_RPMS := \
	CGAL \
	FileGDBAPI \
	SFCGAL \
	dumb-init \
	gdal \
	geos \
	google-noto-fonts-extra \
	gpsbabel \
	hanazono-fonts \
	journald-cloudwatch-logs \
	libgeotiff \
	libgta \
	libkml \
	libosmium \
	openstreetmap-carto \
	osmctools \
	osmdbt \
	osmosis \
	osmium-tool \
	osm2pgsql \
	passenger \
	postgis \
	proj \
	protozero \
	pyosmium \
	rack \
	rubygem-libxml-ruby \
	sbt \
	sqlite-pcre \
	tbb

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
	echo RPMBUILD_GPSBABEL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/gpsbabel.spec) >> .env
	echo RPMBUILD_JOURNALD_CLOUDWATCH_LOGS_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/journald-cloudwatch-logs.spec) >> .env
	echo RPMBUILD_LIBGEOTIFF_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/libgeotiff.spec) >> .env
	echo RPMBUILD_LIBKML_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/libkml.spec) >> .env
	echo RPMBUILD_LIBOSMIUM_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/libosmium.spec) >> .env
	echo RPMBUILD_MAPNIK_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/mapnik.spec) >> .env
	echo RPMBUILD_MOD_TILE_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/mod_tile.spec) >> .env
	echo RPMBUILD_OPENSTREETMAP_CARTO_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/openstreetmap-carto.spec) >> .env
	echo RPMBUILD_OSMCTOOLS_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osmctools.spec) >> .env
	echo RPMBUILD_OSMDBT_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osmdbt.spec --define postgres_dotless=$(POSTGRES_DOTLESS)) >> .env
	echo RPMBUILD_OSMIUM_TOOL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osmium-tool.spec) >> .env
	echo RPMBUILD_OSM2PGSQL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osm2pgsql.spec --define postgres_dotless=$(POSTGRES_DOTLESS)) >> .env
	echo RPMBUILD_PASSENGER_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/passenger.spec) >> .env
	echo RPMBUILD_PROJ_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/proj.spec) >> .env
	echo RPMBUILD_POSTGIS_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/postgis.spec --define postgres_dotless=$(POSTGRES_DOTLESS)) >> .env
	echo RPMBUILD_PROTOZERO_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/protozero.spec) >> .env
	echo RPMBUILD_PYOSMIUM_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/python3-osmium.spec) >> .env
	echo RPMBUILD_PYTHON_MAPNIK_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/python-mapnik.spec) >> .env
	echo RPMBUILD_RACK_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/rubygem-rack.spec) >> .env
	echo RPMBUILD_RUBYGEM_LIBXML_RUBY_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/rubygem-libxml-ruby.spec) >> .env
	echo RPMBUILD_SFCGAL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/SFCGAL.spec) >> .env
	echo RPMBUILD_SQLITE_PCRE_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/sqlite-pcre.spec) >> .env
	echo RPMBUILD_TBB_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/tbb.spec) >> .env

## Container targets

# Build containers.
rpmbuild: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild

rpmbuild-cgal: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-cgal

rpmbuild-generic: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-generic

rpmbuild-fonts: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-fonts

rpmbuild-gdal: .env CGAL FileGDBAPI SFCGAL geos gpsbabel libgeotiff libkml proj sqlite
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-gdal

rpmbuild-gpsbabel: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-gpsbabel

rpmbuild-libgeotiff: .env proj
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-libgeotiff

rpmbuild-libkml: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-libkml

rpmbuild-libosmium: .env protozero
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-libosmium

rpmbuild-journald-cloudwatch-logs: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-journald-cloudwatch-logs

rpmbuild-mapnik: .env gdal postgis
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-mapnik

rpmbuild-mod_tile: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-mod_tile

rpmbuild-openstreetmap-carto: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-openstreetmap-carto

rpmbuild-osmctools: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-osmctools

rpmbuild-osmdbt: .env libosmium
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-osmdbt

rpmbuild-osmium-tool: .env libosmium
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-osmium-tool

rpmbuild-osm2pgsql: .env libosmium postgis
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-osm2pgsql

rpmbuild-passenger: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-passenger

rpmbuild-pgdg: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-pgdg

rpmbuild-postgis: .env gdal
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-postgis

rpmbuild-proj: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-proj

rpmbuild-protozero: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-protozero

rpmbuild-pyosmium: .env libosmium
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-pyosmium

rpmbuild-python-mapnik: .env mapnik
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-python-mapnik

rpmbuild-rack: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-rack

rpmbuild-rubygem-libxml-ruby: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-rubygem-libxml-ruby

rpmbuild-sfcgal: .env $(CGAL_RPM)
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-sfcgal

rpmbuild-sqlite-pcre: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-sqlite-pcre

rpmbuild-tbb: .env
	DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) up -d rpmbuild-tbb

## RPM targets

CGAL: rpmbuild-cgal $(CGAL_RPM)
FileGDBAPI: rpmbuild-generic $(FILEGDBAPI_RPM)
SFCGAL: rpmbuild-sfcgal $(SFCGAL_RPM)
dumb-init: rpmbuild-generic $(DUMB_INIT_RPM)
gdal: rpmbuild-gdal $(GDAL_RPM)
geos: rpmbuild-generic $(GEOS_RPM)
google-noto-fonts-extra: rpmbuild-fonts $(GOOGLE_NOTO_RPM)
gpsbabel: rpmbuild-gpsbabel $(GPSBABEL_RPM)
hanazono-fonts: rpmbuild-fonts $(HANAZONO_RPM)
journald-cloudwatch-logs: rpmbuild-journald-cloudwatch-logs $(JOURNALD_CLOUDWATCH_LOGS_RPM)
libgeotiff: rpmbuild-libgeotiff $(LIBGEOTIFF_RPM)
libgta: rpmbuild-generic $(LIBGTA_RPM)
libkml: rpmbuild-libkml $(LIBKML_RPM)
libosmium: rpmbuild-libosmium $(LIBOSMIUM_RPM)
mapnik: rpmbuild-mapnik $(MAPNIK_RPM)
mod_tile: rpmbuild-mod_tile $(MOD_TILE_RPM)
openstreetmap-carto: rpmbuild-openstreetmap-carto $(OPENSTREETMAP_CARTO_RPM)
osmctools: rpmbuild-osmctools $(OSMCTOOLS_RPM)
osmdbt: rpmbuild-osmdbt $(OSMDBT_RPM)
osmium-tool: rpmbuild-osmium-tool $(OSMIUM_TOOL_RPM)
osmosis: rpmbuild-generic $(OSMOSIS_RPM)
osm2pgsql: rpmbuild-osm2pgsql $(OSM2PGSQL_RPM)
passenger: rpmbuild-passenger $(PASSENGER_RPM)
postgis: rpmbuild-postgis $(POSTGIS_RPM)
proj: rpmbuild-proj $(PROJ_RPM)
protozero: rpmbuild-protozero $(PROTOZERO_RPM)
pyosmium: rpmbuild-pyosmium $(PYOSMIUM_RPM)
python-mapnik: rpmbuild-python-mapnik $(PYTHON_MAPNIK_RPM)
rack: rpmbuild-rack $(RACK_RPM)
rubygem-libxml-ruby: rpmbuild-rubygem-libxml-ruby $(RUBYGEM_LIBXML_RUBY_RPM)
sbt: rpmbuild-generic $(SBT_RPM)
sqlite-pcre: rpmbuild-sqlite-pcre $(SQLITE_PCRE_RPM)
tbb: rpmbuild-tbb $(TBB_RPM)

## Build patterns
RPMS/x86_64/%.rpm RPMS/noarch/%.rpm:
	$(DOCKER_COMPOSE) exec -T $(call rpmbuild_image,$*) \
	$(shell ./scripts/rpmbuild_util.py $(call rpm_package,$*) --config-file $(COMPOSE_FILE))
