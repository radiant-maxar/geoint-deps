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
LIBKML_RPM := $(call rpm_file,libkml)
LIBOSMIUM_RPM := $(call rpm_file,libosmium)
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
PROTOBUF_C_RPM := $(call rpm_file,protobuf-c)
PROTOBUF_RPM := $(call rpm_file,protobuf)
PROTOZERO_RPM := $(call rpm_file,protozero)
PYOSMIUM_RPM := $(call rpm_file,python3-osmium)
PYTHON_MAPNIK_RPM := $(call rpm_file,python-mapnik)
RACK_RPM := $(call rpm_file,rubygem-rack)
RUBY_RPM := $(call rpm_file,ruby)
RUBYGEM_LIBXML_RUBY_RPM := $(call rpm_file,rubygem-libxml-ruby)
RUBYGEM_PG_RPM := $(call rpm_file,rubygem-pg)
SBT_RPM := $(call rpm_file,sbt,noarch)
SFCGAL_RPM := $(call rpm_file,SFCGAL)
SQLITE_PCRE_RPM := $(call rpm_file,sqlite-pcre)
SQLITE_RPM := $(call rpm_file,sqlite)
TBB_RPM := $(call rpm_file,tbb)

# Build images and RPMs.
RPMBUILD_BASE_IMAGES := \
	rpmbuild \
	rpmbuild-fonts \
	rpmbuild-generic \
	rpmbuild-pgdg
RPMBUILD_RPMS := \
	CGAL \
	dumb-init \
	FileGDBAPI \
	gdal \
	geos \
	google-noto-fonts-extra \
	gpsbabel \
	hanazono-fonts \
	journald-cloudwatch-logs \
	libgeotiff \
	libkml \
	libosmium \
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
	protobuf \
	protobuf-c \
	protozero \
	pyosmium \
	python-mapnik \
	rack \
	ruby \
	rubygem-libxml-ruby \
	rubygem-pg \
	sbt \
	SFCGAL \
	sqlite \
	sqlite-pcre \
	tbb


## General targets
.PHONY: \
	all \
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
	echo RPMBUILD_CGAL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/CGAL.spec) >> .env
	echo RPMBUILD_GDAL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/gdal.spec --define postgres_dotless=$(POSTGRES_DOTLESS)) >> .env
	echo RPMBUILD_GEOS_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/geos.spec) >> .env
	echo RPMBUILD_GPSBABEL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/gpsbabel.spec) >> .env
	echo RPMBUILD_JOURNALD_CLOUDWATCH_LOGS_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/journald-cloudwatch-logs.spec) >> .env
	echo RPMBUILD_LIBGEOTIFF_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/libgeotiff.spec) >> .env
	echo RPMBUILD_LIBKML_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/libkml.spec) >> .env
	echo RPMBUILD_LIBOSMIUM_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/libosmium.spec) >> .env
	echo RPMBUILD_MAPNIK_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/mapnik.spec) >> .env
	echo RPMBUILD_OGDI_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/ogdi.spec) >> .env
	echo RPMBUILD_OPENSTREETMAP_CARTO_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/openstreetmap-carto.spec) >> .env
	echo RPMBUILD_OSM2PGSQL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osm2pgsql.spec --define postgres_dotless=$(POSTGRES_DOTLESS)) >> .env
	echo RPMBUILD_OSMCTOOLS_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osmctools.spec) >> .env
	echo RPMBUILD_OSMDBT_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osmdbt.spec --define postgres_dotless=$(POSTGRES_DOTLESS)) >> .env
	echo RPMBUILD_OSMIUM_TOOL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osmium-tool.spec) >> .env
	echo RPMBUILD_PASSENGER_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/passenger.spec) >> .env
	echo RPMBUILD_POSTGIS_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/postgis.spec --define postgres_dotless=$(POSTGRES_DOTLESS)) >> .env
	echo RPMBUILD_PROJ_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/proj.spec) >> .env
	echo RPMBUILD_PROTOBUF_C_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/protobuf-c.spec) >> .env
	echo RPMBUILD_PROTOBUF_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/protobuf.spec) >> .env
	echo RPMBUILD_PROTOZERO_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/protozero.spec) >> .env
	echo RPMBUILD_PYOSMIUM_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/python3-osmium.spec) >> .env
	echo RPMBUILD_PYTHON_MAPNIK_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/python-mapnik.spec) >> .env
	echo RPMBUILD_RACK_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/rubygem-rack.spec) >> .env
	echo RPMBUILD_RUBY_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/ruby.spec) >> .env
	echo RPMBUILD_RUBYGEM_LIBXML_RUBY_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/rubygem-libxml-ruby.spec) >> .env
	echo RPMBUILD_RUBYGEM_PG_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/rubygem-pg.spec --define postgres_dotless=$(POSTGRES_DOTLESS)) >> .env
	echo RPMBUILD_SFCGAL_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/SFCGAL.spec) >> .env
	echo RPMBUILD_SQLITE_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/sqlite.spec) >> .env
	echo RPMBUILD_SQLITE_PCRE_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/sqlite-pcre.spec) >> .env
	echo RPMBUILD_TBB_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/tbb.spec) >> .env


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
CGAL: $(CGAL_RPM)
dumb-init: rpmbuild-generic $(DUMB_INIT_RPM)
FileGDBAPI: rpmbuild-generic $(FILEGDBAPI_RPM)
gdal: $(FILEGDBAPI_RPM) $(GEOS_RPM) $(GPSBABEL_RPM) $(LIBKML_RPM) $(OGDI_RPM) $(CGAL_RPM) $(SFCGAL_RPM) $(SQLITE_RPM) $(PROJ_RPM) $(LIBGEOTIFF_RPM) $(GDAL_RPM)
geos: $(GEOS_RPM)
google-noto-fonts-extra: rpmbuild-fonts $(GOOGLE_NOTO_RPM)
gpsbabel: $(GPSBABEL_RPM)
hanazono-fonts: rpmbuild-fonts $(HANAZONO_RPM)
journald-cloudwatch-logs: $(JOURNALD_CLOUDWATCH_LOGS_RPM)
libgeotiff: $(SQLITE_RPM) $(PROJ_RPM) $(LIBGEOTIFF_RPM)
libkml: $(LIBKML_RPM)
libosmium: $(PROTOBUF_RPM) $(PROTOZERO_RPM) $(LIBOSMIUM_RPM)
mapnik: $(FILEGDBAPI_RPM) $(GEOS_RPM) $(GPSBABEL_RPM) $(LIBKML_RPM) $(OGDI_RPM) $(CGAL_RPM) $(SFCGAL_RPM) $(SQLITE_RPM) $(PROJ_RPM) $(LIBGEOTIFF_RPM) $(GDAL_RPM) $(PROTOBUF_RPM) $(PROTOBUF_C_RPM) $(POSTGIS_RPM) $(MAPNIK_RPM)
ogdi: $(OGDI_RPM)
openstreetmap-carto: $(OPENSTREETMAP_CARTO_RPM)
osm2pgsql: $(FILEGDBAPI_RPM) $(GEOS_RPM) $(GPSBABEL_RPM) $(LIBKML_RPM) $(OGDI_RPM) $(CGAL_RPM) $(SFCGAL_RPM) $(SQLITE_RPM) $(PROJ_RPM) $(LIBGEOTIFF_RPM) $(GDAL_RPM) $(PROTOBUF_RPM) $(PROTOBUF_C_RPM) $(POSTGIS_RPM) $(PROTOZERO_RPM) $(LIBOSMIUM_RPM) $(OSM2PGSQL_RPM)
osmctools: $(OSMCTOOLS_RPM)
osmdbt: $(PROTOBUF_RPM) $(PROTOZERO_RPM) $(LIBOSMIUM_RPM) $(OSMDBT_RPM)
osmium-tool: $(PROTOBUF_RPM) $(PROTOZERO_RPM) $(LIBOSMIUM_RPM) $(OSMIUM_TOOL_RPM)
osmosis: rpmbuild-generic $(OSMOSIS_RPM)
passenger: $(PASSENGER_RPM)
postgis: $(FILEGDBAPI_RPM) $(GEOS_RPM) $(GPSBABEL_RPM) $(LIBKML_RPM) $(OGDI_RPM) $(CGAL_RPM) $(SFCGAL_RPM) $(SQLITE_RPM) $(PROJ_RPM) $(LIBGEOTIFF_RPM) $(GDAL_RPM) $(PROTOBUF_RPM) $(PROTOBUF_C_RPM) $(POSTGIS_RPM)
proj: $(SQLITE_RPM) $(PROJ_RPM)
protobuf-c: $(PROTOBUF_RPM) $(PROTOBUF_C_RPM)
protobuf: $(PROTOBUF_RPM)
protozero: $(PROTOBUF_RPM) $(PROTOZERO_RPM)
pyosmium: $(PROTOBUF_RPM) $(PROTOZERO_RPM) $(LIBOSMIUM_RPM) $(PYOSMIUM_RPM)
python-mapnik: $(FILEGDBAPI_RPM) $(GEOS_RPM) $(GPSBABEL_RPM) $(LIBKML_RPM) $(OGDI_RPM) $(CGAL_RPM) $(SFCGAL_RPM) $(SQLITE_RPM) $(PROJ_RPM) $(LIBGEOTIFF_RPM) $(GDAL_RPM) $(PROTOBUF_RPM) $(PROTOBUF_C_RPM) $(POSTGIS_RPM) $(MAPNIK_RPM) $(PYTHON_MAPNIK_RPM)
rack: $(RACK_RPM)
ruby: $(RUBY_RPM)
rubygem-libxml-ruby: $(RUBYGEM_LIBXML_RUBY_RPM)
rubygem-pg: $(RUBYGEM_PG_RPM)
sbt: rpmbuild-generic $(SBT_RPM)
SFCGAL: $(CGAL_RPM) $(SFCGAL_RPM)
sqlite-pcre: $(SQLITE_RPM) $(SQLITE_PCRE_RPM)
sqlite: $(SQLITE_RPM)
tbb: $(TBB_RPM)


## Build patterns
RPMS/x86_64/%.rpm RPMS/noarch/%.rpm: | .env
	$(MAKE) $(call rpmbuild_image_parent,$*)
	$(call pull_if_ci,$(call rpmbuild_image,$*))
	$(call build_unless_image_exists,$(call rpmbuild_image,$*))
	$(DOCKER_COMPOSE) run --rm -T $(call rpmbuild_image,$*) \
		$(shell ./scripts/rpmbuild_util.py $(call rpm_package,$*) --config-file $(COMPOSE_FILE))
