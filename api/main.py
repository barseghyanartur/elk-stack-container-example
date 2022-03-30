import json
import os
import logging
from logging import getLevelName

from django_micro import configure, route, run

# ************************************************************************
# *************************** django settings ****************************
# ************************************************************************

__author__ = "Artur Barseghyan"
__copyright__ = "2020-2022 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"


DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGS_DIR_NAME = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
)

if not os.path.exists(LOGS_DIR_NAME):
    os.mkdir(LOGS_DIR_NAME)

INSTALLED_APPS = [
    "rest_framework",
    "drf_spectacular",
    "elasticapm.contrib.django",
    "django_extensions",
]

ELASTIC_APM = {
    # Set required service name. Allowed characters:
    # a-z, A-Z, 0-9, -, _, and space
    "SERVICE_NAME": "apm",
    # Use if APM Server requires a token
    "SECRET_TOKEN": "",
    # Set custom APM Server URL (default: http://localhost:8200)
    "SERVER_URL": "http://apm:8200",
    "DEBUG": True,
}

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Ingest API",
    "DESCRIPTION": "Ingest API documentation.",
    "VERSION": "0.1",
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "SERVE_INCLUDE_SCHEMA": False,
    # CDNs for swagger and redoc. You can change the version or even host your
    # own depending on your requirements.
    'SWAGGER_UI_DIST': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest',
    'SWAGGER_UI_FAVICON_HREF': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/favicon-32x32.png',
    'REDOC_DIST': 'https://cdn.jsdelivr.net/npm/redoc@latest',
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(levelname)s %(asctime)s %(request_id)s %(pathname)s "
            "%(name)s %(funcName)s %(lineno)s %(message)s "
            "%(special)s",
        },
    },
    "filters": {"request_id": {"()": "log_request_id.filters.RequestIDFilter"}},
    "root": {
        "level": "DEBUG",
        "filters": ["request_id"],
        "handlers": ["console", "json", "elasticapm"],
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "filters": ["request_id"],
            "level": "DEBUG",
        },
        "json": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filters": ["request_id"],
            "level": "DEBUG",
            "filename": os.path.join(LOGS_DIR_NAME, "json.log"),
            "maxBytes": 1048576,
            "backupCount": 99,
        },
        "elasticapm": {
            "level": "WARNING",
            "class": "elasticapm.contrib.django.handlers.LoggingHandler",
        },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console"],
        },
    },
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


MIDDLEWARE = [
    "log_request_id.middleware.RequestIDMiddleware",  # This should be at the top
    "elasticapm.contrib.django.middleware.TracingMiddleware",
    "elasticapm.contrib.django.middleware.Catch404Middleware",
    "elasticapm.contrib.django.middleware.ErrorIdMiddleware",
]

SECRET_KEY = "123456"

configure(locals(), django_admin=True)

LOGGER = logging.getLogger(__name__)

# ************************************************************************
# ***************************** django views *****************************
# ************************************************************************

from django.contrib import admin
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions


def _debug(request):
    LOGGER.debug(request.data)


def _info(request):
    LOGGER.info(request.data)


def _warning(request):
    LOGGER.warning(request.data)


def _error(request):
    try:
        json.dumps(APIView)
    except Exception as err:
        LOGGER.exception(err, extra=request.data)


_LEVEL_NAME_MAPPING = {
    getLevelName(logging.DEBUG): _debug,
    getLevelName(logging.INFO): _info,
    getLevelName(logging.WARNING): _warning,
    getLevelName(logging.ERROR): _error,
}


class LogView(ViewSet):
    """Log view."""

    permission_classes = [permissions.AllowAny]

    @action(methods=["get", "post"], detail=False, name="log")
    def log(self, request):
        """Current request."""
        if (
            "levelname" in request.data
            and request.data["levelname"] in _LEVEL_NAME_MAPPING
        ):
            func = _LEVEL_NAME_MAPPING[request.data["levelname"]]
            request.data.pop("levelname")
            func(request)
        else:
            _warning(request)
            _info(request)
            _debug(request)
            _error(request)

        return Response(request.data)

    @action(methods=["get", "post"], detail=False, name="error", url_path="log/error")
    def error(self, request):
        """Throw an exception."""
        json.loads(APIView)


# ************************************************************************
# **************************** django routes *****************************
# ************************************************************************
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", LogView, basename="log")
# urlpatterns = [
#     path("log/", LogView.as_view()),
# ]
urlpatterns = [
    path("", include(router.urls)),
    # Optional schema UI:
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="api-swagger"),
    path("redoc/", SpectacularRedocView.as_view(url_name="api-schema"), name="api-redoc"),
]

route("admin/", admin.site.urls),
route("api/", include(urlpatterns)),

if __name__ == "__main__":
    application = run()
