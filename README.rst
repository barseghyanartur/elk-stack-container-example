ELK stack
=========
ELK stack (example) with Docker.

Aim of this repository is to provide a minimalistic example of how to
set up an ELK cluster for local development. For sake of simplicity, all
config files are kept in root (and have been brought down to minimum).

Usage
-----
**Using Docker**

.. code-block:: shell

    make run

Services
--------
The following services are available.

- `Elasticsearch <http://localhost:9200/>`__
- `Kibana <http://localhost:5601/>`__
- Logstash (on port 5044)
- Filebeat
- APM (on port 8200)
- `Sample ingest API (Django based) <http://localhost:8000/api/log/>`__

Add messages to Logstash
------------------------
**Generate some logs**

.. code-block:: shell

    make ingest-logs

**Generate some logs with parameters**

.. code-block:: shell

    make bash
    python /usr/src/app/ingest.py --no-random-time --offset=51 --amount=10

**Ingest logs using sample ingest API**

Make a POST request to the following endpoint: http://localhost:8000/api/log/

.. code-block:: json

    {
        "id": "39",
        "action": "Classified",
        "success": "true"
    }

To enforce a certain log level (available options ``DEBUG``, ``INFO``,
``WARNING``, ``ERROR``), do as follows:

.. code-block:: json

    {
        "id": "39",
        "action": "Classified",
        "success": "true",
        "levelname": "ERROR"
    }

**Force an unhandled exception**

Make a POST request to the following endpoint: http://localhost:8000/api/log/error/

.. code-block:: json

    {
        "id": "39",
        "action": "Classified",
        "success": "true"
    }
