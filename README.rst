ELK stack
=========
ELK stack (example) with Docker (or Podman).

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
- Logstash
- Filebeat
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
