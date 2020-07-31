# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2018 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

""" There are 3 ways to override GeoNode settings:
   1. Using environment variables, if your changes to GeoNode are minimal.
   2. Creating a downstream project, if you are doing a lot of customization.
   3. Override settings in a local_settings.py file, legacy.
"""

import ast
import os
from urlparse import urlparse, urlunparse
from geonode.settings import *

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(PROJECT_ROOT, "uploaded"))

STATIC_ROOT = os.getenv('STATIC_ROOT',
                        os.path.join(PROJECT_ROOT, "static_root")
                        )

# SECRET_KEY = '************************'
# Make this unique, and don't share it with anybody.
SECRET_KEY = os.getenv('SECRET_KEY', "{{ secret_key }}")


# per-deployment settings should go here
SITE_HOST_NAME = os.getenv('SITE_HOST_NAME', 'localhost')
SITE_HOST_PORT = os.getenv('SITE_HOST_PORT', "80")


#SITEURL = os.getenv('SITEURL', "http://%s:%s/" % (SITE_HOST_NAME, SITE_HOST_PORT))

SITEURL = 'https://geoportal.ermis-f.eu'

STATIC_ROOT = os.getenv('STATIC_ROOT',
                        os.path.join("/home/geonode/ermis/ermis", "static_root")
                        )


# we need hostname for deployed
_surl = urlparse(SITEURL)
HOSTNAME = _surl.hostname


# add trailing slash to site url. geoserver url will be relative to this
if not SITEURL.endswith('/'):
    SITEURL = '{}/'.format(SITEURL)

ALLOWED_HOSTS = [HOSTNAME, 'localhost','geoportal.ermis-f.eu','kb.ermis-f.eu','84.205.200.65','84.205.200.65:80','195.251.137.130','195.251.137.90','::1']
PROXY_ALLOWED_HOSTS = ("127.0.0.1",'geoportal.ermis-f.eu','kb.ermis-f.eu','84.205.200.65','84.205.200.65:80','195.251.137.130','195.251.137.90','nominatim.openstreetmap.org','b.tile.openstreetmap.org', 'localhost', '::1')

POSTGIS_VERSION = (2, 0, 7)
#Define email service on GeoNode
EMAIL_ENABLE = False

if EMAIL_ENABLE:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 25
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False
    DEFAULT_FROM_EMAIL = '{{ project_name }} <no-reply@{{ project_name }}>'

TIME_ZONE = 'Europe/Athens'#'UTC'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'geonode',
        'USER': 'geonode',
        'PASSWORD': 'geonode',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_TOUT': 900,
    },
    # vector datastore for uploads
    'datastore': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # 'ENGINE': '', # Empty ENGINE name disables
        'NAME': 'geonode_data',
        'USER': 'geonode',
        'PASSWORD': 'geonode',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_TOUT': 900,
    }
}

GEOSERVER_LOCATION = os.getenv(
    'GEOSERVER_LOCATION', 'https://geoportal.ermis-f.eu/geoserver/'
)

GEOSERVER_PUBLIC_HOST = os.getenv(
    'GEOSERVER_PUBLIC_HOST', SITE_HOST_NAME
)

GEOSERVER_PUBLIC_PORT = os.getenv(
    'GEOSERVER_PUBLIC_PORT', 80
)

GEOSERVER_PUBLIC_LOCATION = os.getenv(
 #   'GEOSERVER_PUBLIC_LOCATION', 'http://{}:{}/geoserver/'.format(GEOSERVER_PUBLIC_HOST, GEOSERVER_PUBLIC_PORT)
	'GEOSERVER_PUBLIC_LOCATION', 'https://geoportal.ermis-f.eu/geoserver/'
)

OGC_SERVER_DEFAULT_USER = os.getenv(
    'GEOSERVER_ADMIN_USER', 'admin'
)

OGC_SERVER_DEFAULT_PASSWORD = os.getenv(
    'GEOSERVER_ADMIN_PASSWORD', 'erm_F2018'
)

# OGC (WMS/WFS/WCS) Server Settings
OGC_SERVER = {
    'default': {
        'BACKEND': 'geonode.geoserver',
        'LOCATION': GEOSERVER_LOCATION,
        'LOGIN_ENDPOINT': 'j_spring_oauth2_geonode_login',
        'LOGOUT_ENDPOINT': 'j_spring_oauth2_geonode_logout',
        # PUBLIC_LOCATION needs to be kept like this because in dev mode
        # the proxy won't work and the integration tests will fail
        # the entire block has to be overridden in the local_settings
        'PUBLIC_LOCATION': GEOSERVER_PUBLIC_LOCATION,
        'USER': OGC_SERVER_DEFAULT_USER,
        'PASSWORD': OGC_SERVER_DEFAULT_PASSWORD,
        'MAPFISH_PRINT_ENABLED': True,
        'PRINT_NG_ENABLED': True,
        'GEONODE_SECURITY_ENABLED': True,
        'GEOFENCE_SECURITY_ENABLED': True,
        'GEOGIG_ENABLED': False,
        'WMST_ENABLED': False,
        'BACKEND_WRITE_ENABLED': True,
        'WPS_ENABLED': False,
        'LOG_FILE': '%s/geoserver/data/logs/geoserver.log' % os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir)),
        # Set to dictionary identifier of database containing spatial data in DATABASES dictionary to enable
        'DATASTORE': 'datastore',
        'PG_GEOGIG': False,
        'TIMEOUT': 60  # number of seconds to allow for HTTP requests
    }
}

# WARNING: Map Editing is affected by this. GeoExt Configuration is cached for 5 minutes
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '/var/tmp/django_cache',
#     }
# }

# If you want to enable Mosaics use the following configuration
UPLOADER = {
    #'BACKEND': 'geonode.rest',
    'BACKEND': 'geonode.importer',
    'OPTIONS': {
        'TIME_ENABLED': True,
        'MOSAIC_ENABLED': False,
        'GEOGIG_ENABLED': False,
    },
    'SUPPORTED_CRS': [
        'EPSG:4326',
        'EPSG:3785',
        'EPSG:3857',
        'EPSG:32647',
        'EPSG:32736',
	'EPSG:2100'
    ],
    'SUPPORTED_EXT': [
        '.shp',
        '.csv',
        '.kml',
        '.kmz',
        '.json',
        '.geojson',
        '.tif',
        '.tiff',
        '.geotiff',
        '.gml',
        '.xml'
    ]
}

CATALOGUE = {
    'default': {
        # The underlying CSW implementation
        # default is pycsw in local mode (tied directly to GeoNode Django DB)
        'ENGINE': 'geonode.catalogue.backends.pycsw_local',
        # pycsw in non-local mode
        # 'ENGINE': 'geonode.catalogue.backends.pycsw_http',
        # GeoNetwork opensource
        # 'ENGINE': 'geonode.catalogue.backends.geonetwork',
        # deegree and others
        # 'ENGINE': 'geonode.catalogue.backends.generic',

        # The FULLY QUALIFIED base url to the CSW instance for this GeoNode
        'URL': '%scatalogue/csw' % SITEURL,
        # 'URL': 'http://localhost:8080/geonetwork/srv/en/csw',
        # 'URL': 'http://localhost:8080/deegree-csw-demo-3.0.4/services',

        # login credentials (for GeoNetwork)
        'USER': 'admin',
        'PASSWORD': 'admin',
        'ALTERNATES_ONLY': True,
    }
}

# pycsw settings
PYCSW = {
    # pycsw configuration
    'CONFIGURATION': {
        # uncomment / adjust to override server config system defaults
        # 'server': {
        #    'maxrecords': '10',
        #    'pretty_print': 'true',
        #    'federatedcatalogues': 'http://catalog.data.gov/csw'
        # },
        'metadata:main': {
            'identification_title': 'GeoNode Catalogue',
            'identification_abstract': 'GeoNode is an open source platform' \
            ' that facilitates the creation, sharing, and collaborative use' \
            ' of geospatial data',
            'identification_keywords': 'sdi, catalogue, discovery, metadata,' \
            ' GeoNode',
            'identification_keywords_type': 'theme',
            'identification_fees': 'None',
            'identification_accessconstraints': 'None',
            'provider_name': 'Organization Name',
            'provider_url': SITEURL,
            'contact_name': 'Lastname, Firstname',
            'contact_position': 'Position Title',
            'contact_address': 'Mailing Address',
            'contact_city': 'City',
            'contact_stateorprovince': 'Administrative Area',
            'contact_postalcode': 'Zip or Postal Code',
            'contact_country': 'Country',
            'contact_phone': '+xx-xxx-xxx-xxxx',
            'contact_fax': '+xx-xxx-xxx-xxxx',
            'contact_email': 'Email Address',
            'contact_url': 'Contact URL',
            'contact_hours': 'Hours of Service',
            'contact_instructions': 'During hours of service. Off on ' \
            'weekends.',
            'contact_role': 'pointOfContact',
        },
        'metadata:inspire': {
            'enabled': 'true',
            'languages_supported': 'eng,gre',
            'default_language': 'eng',
            'date': 'YYYY-MM-DD',
            'gemet_keywords': 'Utility and governmental services',
            'conformity_service': 'notEvaluated',
            'contact_name': 'Organization Name',
            'contact_email': 'Email Address',
            'temp_extent': 'YYYY-MM-DD/YYYY-MM-DD',
        }
    }
}

# GeoNode javascript client configuration

# default map projection
# Note: If set to EPSG:4326, then only EPSG:4326 basemaps will work.
DEFAULT_MAP_CRS = "EPSG:3857"
#DEFAULT_MAP_CRS= "EPSG:2100"

DEFAULT_LAYER_FORMAT = "image/png8"

# Where should newly created maps be focused?
DEFAULT_MAP_CENTER = (28,38)

# How tightly zoomed should newly created maps be?
# 0 = entire world;
# maximum zoom is between 12 and 15 (for Google Maps, coverage varies by area)
DEFAULT_MAP_ZOOM = 6

# Default preview library
# GEONODE_CLIENT_LAYER_PREVIEW_LIBRARY = 'geoext'  # DEPRECATED use HOOKSET instead
GEONODE_CLIENT_HOOKSET = "geonode.client.hooksets.GeoExtHookSet"

# To enable the REACT based Client enable those
# INSTALLED_APPS += ('geonode-client', )
# GEONODE_CLIENT_LAYER_PREVIEW_LIBRARY = 'react'  # DEPRECATED use HOOKSET instead
# GEONODE_CLIENT_HOOKSET = "geonode.client.hooksets.ReactHookSet"

# To enable the Leaflet based Client enable those
# GEONODE_CLIENT_LAYER_PREVIEW_LIBRARY = 'leaflet'  # DEPRECATED use HOOKSET instead
# GEONODE_CLIENT_HOOKSET = "geonode.client.hooksets.LeafletHookSet"

# To enable the MapStore2 based Client enable those
# INSTALLED_APPS += ('geonode_mapstore_client', )
# GEONODE_CLIENT_LAYER_PREVIEW_LIBRARY = 'mapstore'  # DEPRECATED use HOOKSET instead
# GEONODE_CLIENT_HOOKSET = "geonode_mapstore_client.hooksets.MapStoreHookSet"

# LEAFLET_CONFIG = {
#    'TILES': [
#        # Find tiles at:
#        # http://leaflet-extras.github.io/leaflet-providers/preview/
#
#        # Map Quest
#        ('Map Quest',
#         'http://otile4.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
#         'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> '
#         '&mdash; Map data &copy; '
#         '<a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'),
#        # Stamen toner lite.
#        # ('Watercolor',
#        #  'http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.png',
#        #  'Map tiles by <a href="http://stamen.com">Stamen Design</a>, \
#        #  <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; \
#        #  <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, \
#        #  <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'),
#        # ('Toner Lite',
#        #  'http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.png',
#        #  'Map tiles by <a href="http://stamen.com">Stamen Design</a>, \
#        #  <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; \
#        #  <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, \
#        #  <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'),
#    ],
#    'PLUGINS': {
#        'esri-leaflet': {
#            'js': 'lib/js/esri-leaflet.js',
#            'auto-include': True,
#        },
#        'leaflet-fullscreen': {
#            'css': 'lib/css/leaflet.fullscreen.css',
#            'js': 'lib/js/Leaflet.fullscreen.min.js',
#            'auto-include': True,
#        },
#    },
#    'SRID': 3857,
#    'RESET_VIEW': False
# }

ALT_OSM_BASEMAPS = ast.literal_eval(os.environ.get('ALT_OSM_BASEMAPS', 'False'))
CARTODB_BASEMAPS = ast.literal_eval(os.environ.get('CARTODB_BASEMAPS', 'False'))
STAMEN_BASEMAPS = ast.literal_eval(os.environ.get('STAMEN_BASEMAPS', 'False'))
THUNDERFOREST_BASEMAPS = ast.literal_eval(os.environ.get('THUNDERFOREST_BASEMAPS', 'False'))
#MAPBOX_ACCESS_TOKEN = os.environ.get('MAPBOX_ACCESS_TOKEN', None)
#BING_API_KEY = os.environ.get('BING_API_KEY', None)
#GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', None)

#MAP_BASELAYERS = [{
#    "source": {"ptype": "gxp_olsource"},
#    "type": "OpenLayers.Layer",
#    "args": ["No background"],
#    "name": "background",
#    "visibility": False,
#    "fixed": True,
#    "group":"background"
#},
    # {
    #     "source": {"ptype": "gxp_olsource"},
    #     "type": "OpenLayers.Layer.XYZ",
    #     "title": "TEST TILE",
    #     "args": ["TEST_TILE", "http://test_tiles/tiles/${z}/${x}/${y}.png"],
    #     "name": "background",
    #     "attribution": "&copy; TEST TILE",
    #     "visibility": False,
    #     "fixed": True,
    #     "group":"background"
    # },
#    {
#    "source": {"ptype": "gxp_osmsource"},
#    "type": "OpenLayers.Layer.OSM",
#    "name": "mapnik",
#    "visibility": True,
#    "fixed": True,
#    "group": "background"
#}]

MAP_BASELAYERS = [{
    "source": {"ptype": "gxp_olsource"},
    "type": "OpenLayers.Layer",
    "args": ["No background"],
    "name": "background",
    "visibility": False,
    "scales":[100000,50000,20000],
    "fixed": True,
    "group":"background"
}, {
#    "source": {"ptype": "gxp_olsource"},
#    "type": "OpenLayers.Layer.XYZ",
#    "title": "UNESCO",
#    "args": ["UNESCO", "http://en.unesco.org/tiles/${z}/${x}/${y}.png"],
#    "wrapDateLine": True,
#    "name": "background",
#    "attribution": "&copy; UNESCO",
#    "visibility": False,
#    "scales":[100000,50000,20000],
#    "fixed": True,
#    "group":"background"
#}, {
#    "source": {"ptype": "gxp_olsource"},
#    "type": "OpenLayers.Layer.XYZ",
#    "title": "UNESCO GEODATA",
#    "args": ["UNESCO GEODATA", "http://en.unesco.org/tiles/geodata/${z}/${x}/${y}.png"],
#    "name": "background",
#    "attribution": "&copy; UNESCO",
#    "visibility": False,
#    "scales":[100000,50000,20000],
#    "wrapDateLine": True,
#    "fixed": True,
#    "group":"background"
#}, {
# "source": {"ptype": "gxp_olsource"},
#    "type": "OpenLayers.Layer.XYZ",
#    "title": "ESRI",
#    "args": ["ESRI", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}"],
#    "name": "background",
#    "attribution": "&copy; ESRI",
#    "visibility": False,
#    "wrapDateLine": True,
#    "fixed": True,
#    "group":"background"
#}, {
#    "source": {"ptype": "gxp_olsource"},
#    "type": "OpenLayers.Layer.XYZ",
#    "title": "Humanitarian OpenStreetMap",
#    "args": ["Humanitarian OpenStreetMap", "http://a.tile.openstreetmap.fr/hot/${z}/${x}/${y}.png"],
#    "name": "background",
#    "attribution": "&copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a>, Tiles courtesy of <a href='http://hot.openstreetmap.org/' target='_blank'>Humanitarian OpenStreetMap Team</a>",
#    "visibility": False,
#    "wrapDateLine": True,
#    "fixed": True,
#    "group":"background"
# }, {
#     "source": {"ptype": "gxp_olsource"},
#     "type": "OpenLayers.Layer.XYZ",
#     "title": "MapBox Satellite Streets",
#     "args": ["MapBox Satellite Streets", "http://api.mapbox.com/styles/v1/mapbox/satellite-streets-v9/tiles/${z}/${x}/${y}?access_token="+MAPBOX_ACCESS_TOKEN],
#     "name": "background",
#     "attribution": "&copy; <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> &copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <a href='https://www.mapbox.com/feedback/' target='_blank'>Improve this map</a>",
#     "visibility": False,
#     "wrapDateLine": True,
#     "fixed": True,
#     "group":"background"
#}, {
#     "source": {"ptype": "gxp_olsource"},
#     "type": "OpenLayers.Layer.XYZ",
#     "title": "MapBox Streets",
#     "args": ["MapBox Streets", "http://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/${z}/${x}/${y}?access_token="+MAPBOX_ACCESS_TOKEN],
#     "name": "background",
#     "attribution": "&copy; <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> &copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <a href='https://www.mapbox.com/feedback/' target='_blank'>Improve this map</a>",
#     "visibility": False,
#     "wrapDateLine": True,
#     "fixed": True,
#     "group":"background"
#}, {
#    "source": {"ptype": "gxp_osmsource"},
#    "type": "OpenLayers.Layer.OSM",
#    "title": "OpenStreetMap",
#    "name": "mapnik",
#    "attribution": "&copy; <a href='http://osm.org/copyright'>OpenStreetMap</a> contributors",
#    "visibility": True,
#    "wrapDateLine": True,
#    "fixed": True,
#   "group": "background"
 "source": {"ptype": "gxp_olsource"},
    "type": "OpenLayers.Layer.XYZ",
    "title": "ESRI Hydro",
    "args": ["ESRI Hydro", "https://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/${z}/${y}/${x}"],
    "name": "background",
    "attribution": "&copy; ESRI",
    "visibility": False,
    "wrapDateLine": True,
     "scales":[100000,50000,20000],
    "fixed": True,
    "group":"background"
}, {
 "source": {"ptype": "gxp_olsource"},
    "type": "OpenLayers.Layer.XYZ",
    "title": "ESRI Satellite",
    "args": ["ESRI Satellite", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/${z}/${y}/${x}"],
    "name": "background",
    "attribution": "&copy; ESRI",
    "visibility": False,
    "wrapDateLine": True,
    "scales":[100000,50000,20000],
    "fixed": True,
    "group":"background"
}, {
 "source": {"ptype": "gxp_olsource"},
    "type": "OpenLayers.Layer.XYZ",
    "title": "ESRI Topo",
    "args": ["ESRI Topo", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/${z}/${y}/${x}"],
    "name": "background",
    "attribution": "&copy; ESRI",
    "visibility": True,
    "scales":[100000,50000,20000],
    "wrapDateLine": True,
    "fixed": True,
    "group":"background"
}]

if 'geonode.geoserver' in INSTALLED_APPS:
    LOCAL_GEOSERVER = {
        "source": {
            "ptype": "gxp_wmscsource",
            "url": OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms",
            "restUrl": "/gs/rest"
        }
    }
    baselayers = MAP_BASELAYERS
    MAP_BASELAYERS = [LOCAL_GEOSERVER]
    MAP_BASELAYERS.extend(baselayers)

# To enable the REACT based Client enable those
# INSTALLED_APPS += ('geonode-client', )
# GEONODE_CLIENT_LAYER_PREVIEW_LIBRARY = 'react'  # DEPRECATED use HOOKSET instead
# GEONODE_CLIENT_HOOKSET = "geonode.client.hooksets.ReactHookSet"

# To enable the Leaflet based Client enable those
# GEONODE_CLIENT_LAYER_PREVIEW_LIBRARY = 'leaflet'  # DEPRECATED use HOOKSET instead
# GEONODE_CLIENT_HOOKSET = "geonode.client.hooksets.LeafletHookSet"

# To enable the MapLoom based Client enable those
# GEONODE_CLIENT_LAYER_PREVIEW_LIBRARY = 'maploom'  # DEPRECATED use HOOKSET instead
# GEONODE_CLIENT_HOOKSET = "geonode.client.hooksets.MaploomHookSet"
#
# CORS_ORIGIN_WHITELIST = (
#     HOSTNAME
# )

# To enable the MapStore2 based Client enable those
# if 'geonode_mapstore_client' not in INSTALLED_APPS:
#     INSTALLED_APPS += (
#         'mapstore2_adapter',
#         'geonode_mapstore_client',)
# GEONODE_CLIENT_LAYER_PREVIEW_LIBRARY = 'mapstore'  # DEPRECATED use HOOKSET instead
# GEONODE_CLIENT_HOOKSET = "geonode_mapstore_client.hooksets.MapStoreHookSet"
# MAPSTORE_DEBUG = False



if 'geonode.geoserver' in INSTALLED_APPS:
    LOCAL_GEOSERVER = {
        "type": "wms",
        "url": OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms",
        "visibility": True,
        "title": "Local GeoServer",
        "group": "background",
        "format": "image/png8",
        "restUrl": "/gs/rest"
    }
    # baselayers = MAPSTORE_BASELAYERS
    # MAPSTORE_BASELAYERS = [LOCAL_GEOSERVER]
    # MAPSTORE_BASELAYERS.extend(baselayers)

# Use kombu broker by default
# REDIS_URL = 'redis://localhost:6379/1'
# BROKER_URL = REDIS_URL
# CELERY_RESULT_BACKEND = REDIS_URL
CELERYD_HIJACK_ROOT_LOGGER = True
CELERYD_CONCURENCY = 1
# Set this to False to run real async tasks
CELERY_ALWAYS_EAGER = True
CELERYD_LOG_FILE = None
CELERY_REDIRECT_STDOUTS = True
CELERYD_LOG_LEVEL = 1

# Haystack Search Backend Configuration. To enable,
# first install the following:
# - pip install django-haystack
# - pip install elasticsearch==2.4.0
# - pip install woosh
# - pip install pyelasticsearch
# Set HAYSTACK_SEARCH to True
# Run "python manage.py rebuild_index"
# HAYSTACK_SEARCH = False
# Avoid permissions prefiltering
SKIP_PERMS_FILTER = True
# Update facet counts from Haystack
HAYSTACK_FACET_COUNTS = True
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
    #    'db': {
    #        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    #        'EXCLUDED_INDEXES': ['thirdpartyapp.search_indexes.BarIndex'],
    #        }
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s'
        },
        'simple': {
            'format': '%(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"], "level": "ERROR", },
        "geonode": {
            "handlers": ["console"], "level": "INFO", },
        "geonode.qgis_server": {
            "handlers": ["console"], "level": "ERROR", },
        "gsconfig.catalog": {
            "handlers": ["console"], "level": "ERROR", },
        "owslib": {
            "handlers": ["console"], "level": "ERROR", },
        "pycsw": {
            "handlers": ["console"], "level": "INFO", },
        "celery": {
            'handlers': ["console"], 'level': 'ERROR', },
    },
}

# Additional settings
CORS_ORIGIN_ALLOW_ALL = True

GEOIP_PATH = "/usr/local/share/GeoIP"

# add following lines to your local settings to enable monitoring
MONITORING_ENABLED = False

if MONITORING_ENABLED:
    if 'geonode.contrib.monitoring' not in INSTALLED_APPS:
        INSTALLED_APPS += ('geonode.contrib.monitoring',)
    if 'geonode.contrib.monitoring.middleware.MonitoringMiddleware' not in MIDDLEWARE_CLASSES:
        MIDDLEWARE_CLASSES += \
            ('geonode.contrib.monitoring.middleware.MonitoringMiddleware',)
    MONITORING_CONFIG = None
    MONITORING_HOST_NAME = os.getenv("MONITORING_HOST_NAME", HOSTNAME)
    MONITORING_SERVICE_NAME = 'geonode'

#Define email service on GeoNode
EMAIL_ENABLE = False

if EMAIL_ENABLE:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 25
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False
    DEFAULT_FROM_EMAIL = 'Example.com <no-reply@localhost>'

# Documents Thumbnails
UNOCONV_ENABLE = True

if UNOCONV_ENABLE:
    UNOCONV_EXECUTABLE = os.getenv('UNOCONV_EXECUTABLE', '/usr/bin/unoconv')
    UNOCONV_TIMEOUT = os.getenv('UNOCONV_TIMEOUT', 30)  # seconds

# Advanced Security Workflow Settings
ACCOUNT_APPROVAL_REQUIRED = False
CLIENT_RESULTS_LIMIT = 20
API_LIMIT_PER_PAGE = 1000
FREETEXT_KEYWORDS_READONLY = False
RESOURCE_PUBLISHING = False
ADMIN_MODERATE_UPLOADS = False
GROUP_PRIVATE_RESOURCES = False
GROUP_MANDATORY_RESOURCES = False
MODIFY_TOPICCATEGORY = True
USER_MESSAGES_ALLOW_MULTIPLE_RECIPIENTS = True
DISPLAY_WMS_LINKS = True
REGISTRATION_OPEN = False
# For more information on available settings please consult the Django docs at
# https://docs.djangoproject.com/en/dev/ref/settings
# ######################################################################### #
# account registration settings
ACCOUNT_OPEN_SIGNUP = False
ACCOUNT_APPROVAL_REQUIRED = False
ACCOUNT_EMAIL_CONFIRMATION_EMAIL = False
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False

# notification settings
NOTIFICATION_ENABLED = False
NOTIFICATION_LANGUAGE_MODULE = "account.Account"

# Queue non-blocking notifications.
NOTIFICATION_QUEUE_ALL = False

# pinax.notifications
# or notification
NOTIFICATIONS_MODULE = 'pinax.notifications'

#if NOTIFICATION_ENABLED:
   # INSTALLED_APPS += (NOTIFICATIONS_MODULE, )





import ldap
from django_auth_ldap.config import LDAPSearch,GroupOfNamesType, PosixGroupType,NestedGroupOfNamesType

AUTHENTICATION_BACKENDS = (
 #   'oauth2_provider.backends.OAuth2Backend',
#    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django_cas_ng.backends.CASBackend',
	 #   'allauth.account.auth_backends.AuthenticationBackend'
)

CAS_SERVER_URL='http://service.ermis-f.eu/'
CAS_VERSION= '3'
CAS_LOGOUT_COMPLETELY= True
CAS_APPLY_ATTRIBUTES_TO_USER = True
CAS_REDIRECT_URL='https://geoportal.ermis-f.eu'
CAS_RENAME_ATTRIBUTES = {'first_name': 'first_name','last_name':'last_name', 'organization':'organization'}

SESSION_COOKIE_AGE = 36000
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


AUTH_LDAP_SERVER_URI = 'ldap://geoportal.ermis-f.eu:389'
LDAP_SEARCH_DN = 'cn=users,dc=geoportal,dc=ermis-f,dc=eu'
AUTH_LDAP_USER = '(uid=%(user)s)'
AUTH_LDAP_BIND_DN = 'cn=admin,dc=geoportal,dc=ermis-f,dc=eu'
AUTH_LDAP_BIND_PASSWORD = 'Erm_F2018'
	#AUTH_LDAP_BIND_DN = ''
	#AUTH_LDAP_BIND_PASSWORD = ''
AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'first_name','last_name':'last_name','email':'Email'
}
AUTH_LDAP_USER_SEARCH = LDAPSearch(LDAP_SEARCH_DN,
                                   ldap.SCOPE_SUBTREE, AUTH_LDAP_USER)

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    'ou=geonode,dc=geoportal,dc=ermis-f,dc=eu',
    ldap.SCOPE_SUBTREE,
    '(objectClass=groupOfNames)',
)
AUTH_LDAP_GROUP_TYPE =  NestedGroupOfNamesType()
	#AUTH_LDAP_REQUIRE_GROUP = "ou=geonode,dc=ermis-floods-dev,dc=aegean,dc=gr"

AUTH_LDAP_MIRROR_GROUPS=True
AUTH_LDAP_ALWAYS_UPDATE_USER=True
AUTH_LDAP_AUTHORIZE_ALL_USERS=True

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=active,ou=geonode,dc=geoportal,dc=ermis-f,dc=eu",
    "is_staff": "cn=staff,ou=geonode,dc=geoportal,dc=ermis-f,dc=eu",
    "is_superuser": "cn=superuser,ou=geonode,dc=geoportal,dc=ermis-f,dc=eu",
}

AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CONNECTION_OPTIONS = {
ldap.OPT_DEBUG_LEVEL: 3,
ldap.OPT_REFERRALS: 0,
}





#AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
#    'ou=geonode,dc=ermis-floods-dev,dc=aegean,dc=gr',
#    ldap.SCOPE_SUBTREE,
#    '(objectClass=groupOfNames)',
#)
#AUTH_LDAP_GROUP_TYPE =  NestedGroupOfNamesType()
#AUTH_LDAP_REQUIRE_GROUP = "ou=geonode,dc=ermis-floods-dev,dc=aegean,dc=gr"

#AUTH_LDAP_MIRROR_GROUPS=True
#AUTH_LDAP_ALWAYS_UPDATE_USER=True
#AUTH_LDAP_AUTHORIZE_ALL_USERS=True
#
#AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#    "is_active": "cn=active,ou=geonode,dc=ermis-floods-dev,dc=aegean,dc=gr",
#    "is_staff": "cn=staff,ou=geonode,dc=ermis-floods-dev,dc=aegean,dc=gr",
#    "is_superuser": "cn=superuser,ou=geonode,dc=ermis-floods-dev,dc=aegean,dc=gr",
#}

#AUTH_LDAP_FIND_GROUP_PERMS = True
#AUTH_LDAP_CONNECTION_OPTIONS = {
#ldap.OPT_DEBUG_LEVEL: 3,
#ldap.OPT_REFERRALS: 0,
#}
