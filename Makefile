## Conditional variables.
DOCKER ?= docker
DOCKER_COMPOSE ?= docker-compose
CI ?= false
COMPOSE_FILE ?= docker-compose.yml
COMPOSE_PROJECT_NAME ?= geoint-deps-$(RPMBUILD_CHANNEL)
IMAGE_PREFIX ?= $(COMPOSE_PROJECT_NAME)_


## Macro functions.
build_unless_image_exists = $(shell $(DOCKER) image inspect $(IMAGE_PREFIX)$(1) >/dev/null 2>&1 || DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) build $(1))
pull_if_ci = $(shell bash -c '[ "$(CI)" == "false" ] || $(DOCKER_COMPOSE) pull --quiet $(1)')

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
rpmbuild_image_parent = $(call rpmbuild_util,$(call rpmbuild_image,$(1)).build.args.rpmbuild_image,--variable --config-key services)
rpmbuild_release = $(call config_release,$(call rpm_package,$(1)))
rpmbuild_version = $(call config_version,$(call rpm_package,$(1)))


## Variables
DOCKER_VERSION := $(shell $(DOCKER) --version 2>/dev/null)
DOCKER_COMPOSE_VERSION := $(shell $(DOCKER_COMPOSE) --version 2>/dev/null)
POSTGRES_VERSION := $(call rpmbuild_util,postgres_version,--variable)
RPMBUILD_CHANNEL := $(call rpmbuild_util,channel_name,--variable)
RPMBUILD_UID := $(shell id -u)
RPMBUILD_GID := $(shell id -g)

# RPM files at desired versions.
ARMADILLO_RPM := $(call rpm_file,armadillo)
ARPACK_RPM := $(call rpm_file,arpack)
CGAL_RPM := $(call rpm_file,CGAL)
DUMB_INIT_RPM := $(call rpm_file,dumb-init)
FILEGDBAPI_RPM := $(call rpm_file,FileGDBAPI)
G2CLIB_RPM := $(call rpm_file,g2clib)
GDAL_RPM := $(call rpm_file,gdal)
GEOS_RPM := $(call rpm_file,geos)
GOOGLE_NOTO_RPM := $(call rpm_file,google-noto-fonts-extra)
GPSBABEL_RPM := $(call rpm_file,gpsbabel)
HANAZONO_RPM := $(call rpm_file,hanazono-fonts)
INIPARSER_RPM := $(call rpm_file,iniparser)
JOURNALD_CLOUDWATCH_LOGS_RPM := $(call rpm_file,journald-cloudwatch-logs)
LIBGEOTIFF_RPM := $(call rpm_file,libgeotiff)
LIBGTA_RPM := $(call rpm_file,libgta)
LIBKML_RPM := $(call rpm_file,libkml)
LIBOSMIUM_RPM := $(call rpm_file,libosmium)
LIBPQXX_RPM := $(call rpm_file,libpqxx)
MAPNIK_RPM := $(call rpm_file,mapnik)
OGDI_RPM := $(call rpm_file,ogdi)
OPENSTREETMAP_CARTO_RPM := $(call rpm_file,openstreetmap-carto)
OSM2PGSQL_RPM := $(call rpm_file,osm2pgsql)
OSMCTOOLS_RPM := $(call rpm_file,osmctools)
OSMDBT_RPM := $(call rpm_file,osmdbt)
OSMIUM_TOOL_RPM := $(call rpm_file,osmium-tool)
OSMOSIS_RPM := $(call rpm_file,osmosis)
PASSENGER_RPM := $(call rpm_file,passenger)
POSTGIS_RPM := $(call rpm_file,postgis)
PROJ_RPM := $(call rpm_file,proj)
PROTOZERO_RPM := $(call rpm_file,protozero)
PYOSMIUM_RPM := $(call rpm_file,python3-osmium)
PYTHON_MAPNIK_RPM := $(call rpm_file,python3-mapnik)
RACK_RPM := $(call rpm_file,rubygem-rack)
RUBYGEM_LIBXML_RUBY_RPM := $(call rpm_file,rubygem-libxml-ruby)
SBT_RPM := $(call rpm_file,sbt,noarch)
SFCGAL_RPM := $(call rpm_file,SFCGAL)
SQLITE_PCRE_RPM := $(call rpm_file,sqlite-pcre)
URIPARSER_RPM := $(call rpm_file,uriparser)

# Build images and RPMs.
RPMBUILD_BASE_IMAGES := \
	rpmbuild \
	rpmbuild-fonts \
	rpmbuild-generic \
	rpmbuild-pgdg
RPMBUILD_RPMS := \
	armadillo \
	arpack \
	CGAL \
	dumb-init \
	FileGDBAPI \
	g2clib \
	gdal \
	geos \
	google-noto-fonts-extra \
	gpsbabel \
	hanazono-fonts \
	iniparser \
	journald-cloudwatch-logs \
	libgeotiff \
	libgta \
	libkml \
	libosmium \
	libpqxx \
	mapnik \
	ogdi \
	openstreetmap-carto \
	osm2pgsql \
	osmctools \
	osmdbt \
	osmium-tool \
	osmosis \
	passenger \
	postgis \
	proj \
	protozero \
	pyosmium \
	python3-mapnik \
	rack \
	rubygem-libxml-ruby \
	sbt \
	SFCGAL \
	sqlite-pcre \
	uriparser


## General targets
.PHONY: \
	all \
	all-rpms \
	distclean \
	$(RPMBUILD_BASE_IMAGES) \
	$(RPMBUILD_RPMS)

all:
ifndef DOCKER_VERSION
	$(error "command docker is not available, please install Docker")
endif
ifndef DOCKER_COMPOSE_VERSION
	$(error "command docker-compose is not available, please install Docker")
endif

all-rpms: $(RPMBUILD_RPMS)

distclean: .env
	$(DOCKER_COMPOSE) down --volumes --rmi all
	rm -fr .env RPMS/noarch RPMS/x86_64 SOURCES/*.asc SOURCES/*.sha256 SOURCES/*.tgz SOURCES/*.tar.gz SOURCES/*.tar.xz SOURCES/*.zip

# Environment file for docker-compose; required packages for build containers
# are provided here.
.env: SPECS/*.spec
	echo COMPOSE_PROJECT_NAME=$(COMPOSE_PROJECT_NAME) > .env
	echo IMAGE_PREFIX=$(IMAGE_PREFIX) >> .env
	echo RPMBUILD_GID=$(RPMBUILD_GID) >> .env
	echo RPMBUILD_UID=$(RPMBUILD_UID) >> .env
	echo RPMBUILD_ARMADILLO_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/armadillo.spec) >> .env
	echo RPMBUILD_ARPACK_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/arpack.spec) >> .env
	echo RPMBUILD_CGAL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/CGAL.spec) >> .env
	echo RPMBUILD_G2CLIB_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/g2clib.spec) >> .env
	echo RPMBUILD_GDAL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/gdal.spec --define postgres_version=$(POSTGRES_VERSION)) >> .env
	echo RPMBUILD_GPSBABEL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/gpsbabel.spec) >> .env
	echo RPMBUILD_JOURNALD_CLOUDWATCH_LOGS_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/journald-cloudwatch-logs.spec) >> .env
	echo RPMBUILD_LIBGEOTIFF_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/libgeotiff.spec) >> .env
	echo RPMBUILD_LIBKML_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/libkml.spec) >> .env
	echo RPMBUILD_LIBOSMIUM_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/libosmium.spec) >> .env
	echo RPMBUILD_LIBPQXX_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/libpqxx.spec --define postgres_version=$(POSTGRES_VERSION)) >> .env
	echo RPMBUILD_MAPNIK_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/mapnik.spec --define postgres_version=$(POSTGRES_VERSION)) >> .env
	echo RPMBUILD_OGDI_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/ogdi.spec) >> .env
	echo RPMBUILD_OPENSTREETMAP_CARTO_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/openstreetmap-carto.spec) >> .env
	echo RPMBUILD_OSM2PGSQL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osm2pgsql.spec --define postgres_version=$(POSTGRES_VERSION)) >> .env
	echo RPMBUILD_OSMCTOOLS_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osmctools.spec) >> .env
	echo RPMBUILD_OSMDBT_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osmdbt.spec --define postgres_version=$(POSTGRES_VERSION)) >> .env
	echo RPMBUILD_OSMIUM_TOOL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osmium-tool.spec) >> .env
	echo RPMBUILD_PASSENGER_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/passenger.spec) >> .env
	echo RPMBUILD_POSTGIS_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/postgis.spec --define postgres_version=$(POSTGRES_VERSION)) >> .env
	echo RPMBUILD_PROJ_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/proj.spec) >> .env
	echo RPMBUILD_PROTOZERO_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/protozero.spec) >> .env
	echo RPMBUILD_PYOSMIUM_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/python3-osmium.spec) >> .env
	echo RPMBUILD_PYTHON_MAPNIK_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/python3-mapnik.spec) >> .env
	echo RPMBUILD_RACK_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/rubygem-rack.spec) >> .env
	echo RPMBUILD_RUBYGEM_LIBXML_RUBY_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/rubygem-libxml-ruby.spec) >> .env
	echo RPMBUILD_SFCGAL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/SFCGAL.spec) >> .env
	echo RPMBUILD_SQLITE_PCRE_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/sqlite-pcre.spec) >> .env
	echo RPMBUILD_URIPARSER_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/uriparser.spec) >> .env


## Image targets
rpmbuild: .env
	$(call pull_if_ci,$@)
	$(call build_unless_image_exists,$@)

rpmbuild-fonts: rpmbuild
	$(call pull_if_ci,$?)
	$(call pull_if_ci,$@)
	$(call build_unless_image_exists,$@)

rpmbuild-generic: rpmbuild
	$(call pull_if_ci,$?)
	$(call pull_if_ci,$@)
	$(call build_unless_image_exists,$@)

rpmbuild-pgdg: rpmbuild
	$(call pull_if_ci,$?)
	$(call pull_if_ci,$@)
	$(call build_unless_image_exists,$@)


## RPM targets
armadillo: $(ARPACK_RPM) \
           $(ARMADILLO_RPM)
arpack: $(ARPACK_RPM)
CGAL: $(CGAL_RPM)
dumb-init: $(DUMB_INIT_RPM)
FileGDBAPI: $(FILEGDBAPI_RPM)
g2clib: $(G2CLIB_RPM)
gdal: $(ARPACK_RPM) $(CGAL_RPM) $(FILEGDBAPI_RPM) $(GEOS_RPM) $(GPSBABEL_RPM) $(OGDI_RPM) $(PROJ_RPM) $(URIPARSER_RPM) \
      $(ARMADILLO_RPM) $(LIBGEOTIFF_RPM) $(LIBKML_RPM) $(SFCGAL_RPM) \
      $(GDAL_RPM)
geos: $(GEOS_RPM)
google-noto-fonts-extra: rpmbuild-fonts $(GOOGLE_NOTO_RPM)
gpsbabel: $(GPSBABEL_RPM)
hanazono-fonts: rpmbuild-fonts $(HANAZONO_RPM)
iniparser: $(INIPARSER_RPM)
journald-cloudwatch-logs: $(JOURNALD_CLOUDWATCH_LOGS_RPM)
libgeotiff: $(PROJ_RPM) \
            $(LIBGEOTIFF_RPM)
libgta: $(LIBGTA_RPM)
libkml: $(URIPARSER_RPM) \
        $(LIBKML_RPM)
libosmium: $(LIBOSMIUM_RPM)
libpqxx: $(LIBPQXX_RPM)
mapnik: $(MAPNIK_RPM)
ogdi: $(OGDI_RPM)
openstreetmap-carto: $(OPENSTREETMAP_CARTO_RPM)
osm2pgsql: $(OSM2PGSQL_RPM)
osmctools: $(OSMCTOOLS_RPM)
osmdbt: $(OSMDBT_RPM)
osmium-tool: $(OSMIUM_TOOL_RPM)
osmosis: $(OSMOSIS_RPM)
passenger: $(PASSENGER_RPM)
postgis: $(POSTGIS_RPM)
proj: $(PROJ_RPM)
protozero: $(PROTOZERO_RPM)
pyosmium: $(PYOSMIUM_RPM)
python3-mapnik: $(PYTHON_MAPNIK_RPM)
rack: $(RACK_RPM)
rubygem-libxml-ruby: $(RUBYGEM_LIBXML_RUBY_RPM)
sbt: $(SBT_RPM)
SFCGAL: $(CGAL_RPM) \
        $(SFCGAL_RPM)
sqlite-pcre: $(SQLITE_PCRE_RPM)
uriparser: $(URIPARSER_RPM)


## Build patterns
RPMS/x86_64/%.rpm RPMS/noarch/%.rpm: | .env
	$(MAKE) $(call rpmbuild_image_parent,$*)
	$(call pull_if_ci,$(call rpmbuild_image,$*))
	$(call build_unless_image_exists,$(call rpmbuild_image,$*))
	$(DOCKER_COMPOSE) run --rm -T $(call rpmbuild_image,$*) \
	  $(shell ./scripts/rpmbuild_util.py $(call rpm_package,$*) --config-file $(COMPOSE_FILE))
