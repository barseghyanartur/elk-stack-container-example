ELK stack
=========
ELK stack (dev) with Docker (or Podman).

Aim of this repository is to provide a minimalistic example of how to
set up an ELK cluster for local development. For sake of simplicity, all
config files are kept in root (and have been brought down to minimum).

Usage
-----
**Using Docker**

.. code-block:: shell

    docker-compose up

**Using Podman**

.. code-block:: shell

    podman-compose up

If you have issues with ports not being available outside the container, 
run the following command before running ```podman-compose up```:

.. code-block:: shell

    podman-compose down
    podman stop --all

Services
--------
The following services are available.

- `Elasticsearch <http://localhost:9200/>`__
- `Kibana <http://localhost:5601/>`__
- Logstash
- Filebeat

Add messages to Logstash
------------------------
**Install requirements**

.. code-block:: shell

    pip install -r requirements.txt

**Generate some logs**

.. code-block:: shell

    python factories/generate.py --no-random-time --offset=51 --amount=10
