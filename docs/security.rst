Security
========
It's important to understand, that security for each of the components for the
ELK stack is configured separately. For instance, you can password protect
Elasticsearch and still use un-protected Kibana. Same way you could access
Logstash without a password, but since instruct Logstash to use password
protected Elasticsearch.

Minimal security setup is described below briefly, in a form of easily 
reproducible steps.

docker-compose.yml
------------------
**Elasticsearch**

Add ``ELASTIC_PASSWORD=changeme`` to the ``environment`` section and set
the ``xpack.security.enabled`` setting to ``true``.

.. code-block:: yaml

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.5.1
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=true
      - ELASTIC_PASSWORD=changeme
    ports:
      - "9200:9200"
      - "9300:9300"

**Logstash**

Do not enable xpack security for Logstash.

**Kibana**

Add ``./kibana.yml:/usr/share/kibana/config/kibana.yml`` under ``volumes`` and
set the ``xpack.security.enabled`` setting to ``true``.

.. code-block:: yaml

  kibana:
    image: docker.elastic.co/kibana/kibana:7.5.1
    depends_on:
      - logstash
      - elasticsearch
    ports: 
      - 5601:5601
    volumes:
      - ./kibana.yml:/usr/share/kibana/config/kibana.yml
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=true

**Filebeat**

Do not enable xpack security for Filebeat.

kibana.yml
----------
Use here same password defined in ``elasticsearch`` section of the
docker-compose.yml.

.. code-block:: yaml

    server.name: kibana
    server.host: "0"
    elasticsearch.hosts: [ "http://elasticsearch:9200" ]
    elasticsearch.username: elastic
    elasticsearch.password: changeme
    xpack.monitoring.ui.container.elasticsearch.enabled: true
    xpack.security.encryptionKey: "1234567890123456789012345678901234567890"

logstash.conf
-------------
Instruct Logstash about the Elasticsearch credentials.

.. code-block:: yaml

    output {
        elasticsearch {
            hosts => "elasticsearch:9200"
            index => "%{[@metadata][beat]}-%{[@metadata][version]}"
            document_id => "%{fingerprint}"
            user => "elastic"
            password => "changeme"
        }
    }

Kibana Management Interface configuration
-----------------------------------------
You should be able to log into `Kibana <http://localhost:5601/>`__ with your
credentials specified earlier (``elastic:changeme``).

1. Create an index pattern.
2. Create a query.
3. Create a dashboard.
4. Now go to ``Security`` -> ``Roles`` -> ``Add role``.
5. Call it ``read_only_logstash``.

.. code-block:: text

    Elasticsearch:
        Cluster privileges: all
        Run As privileges: (empty)
        Index privileges:
            Indices: filebeat*
            Privileges: read

.. code-block:: text

    Kibana:
        Add space privilege:
           Spaces: Default
           Dashboard: Read

6. Click on ``Create space privilege`` button.
7. Click on ``Create role`` button.
8. Now go to ``Security`` -> ``Users`` -> ``Add user``.
9. Make a new user, call him ``dashboard_only_user``:

.. code-block:: text

    Username: dashboard_only_user
    Password: test1234
    Confirm password: test1234
    Roles: read_only_logstash, kibana_dashboard_only_user

You're done. You might use the ``dashboard_only_user`` credentials to log into
minimalistic (non admin) Kibana interface to view your data.
