import json
import os
import logging

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
]

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
        "handlers": ["console", "json"],
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
]

SECRET_KEY = "123456"

configure(locals(), django_admin=True)

LOGGER = logging.getLogger(__name__)

# ************************************************************************
# ***************************** django views *****************************
# ************************************************************************

from django.contrib import admin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


class LogView(APIView):
    """Log view."""

    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        """Current request."""
        LOGGER.warning(request.data)
        LOGGER.info(request.data)
        LOGGER.debug(request.data)
        try:
            json.dumps(APIView)
        except Exception as err:
            LOGGER.exception(err)

        return Response(request.data)

    post = get


# ************************************************************************
# **************************** django routes *****************************
# ************************************************************************
from django.urls import include, path

urlpatterns = [
    path("log/", LogView.as_view()),
]

route("admin/", admin.site.urls),
route("api/", include(urlpatterns)),

if __name__ == "__main__":
    application = run()
