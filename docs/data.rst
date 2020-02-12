Data
====
Data
----
Logger produces data similar to the following:

.. code-block:: json

    {"date": "2020-02-12T23:54:35.042", "id": "1", "success": "true", "action": "Created"}
    {"date": "2020-02-12T23:54:50.044", "id": "1", "success": "true", "action": "Classified"}
    {"date": "2020-02-12T23:55:05.046", "id": "1", "success": "true", "action": "Explained"}

What we want is to properly index it in the Elasticsearch.

In order to do that, we collect it using Filebeat.

Filebeat
--------
**filebeat.yml**

.. code-block:: yaml

    filebeat.inputs:

      - input_type: log
        paths:
          - /var/log/json*.log*
        tags: ["json"]
        json.keys_under_root: true
        json.add_error_key: true

    output.logstash:
      hosts: ["logstash:5044"]

Some of the code above explained below:

**filebeat.inputs.tags**

Note, that we send additional tag called ``json`` along, so that later (in the
Logstash) we could safely rely on that to determine, what kind of data
structure are we about to be processing (as there may be many types and
formats sent to Logstash at the same time).

.. code-block:: text

    tags: ["json"]

**json.keys_under_root**

This automatically treats log records (string by default) as JSON.

Logstash
--------
**logstash.conf**

.. code-block:: text

    input {
        beats {
            port => 5044
            ssl => false
        }
    }

    filter {
        if "json" in [tags] {
            mutate {
                add_field => {"raw_id" => "%{id}-%{action}-%{date}"}
            }

            fingerprint {
                method => "SHA1"
                source => "raw_id"
            }

            mutate {
                remove_field => ["raw_id"]
            }

            mutate {
                add_field => {"[@metadata][tag]" => "json"}
            }
        }
    }

    output {
        if "json" in [tags] {
            elasticsearch {
                hosts => "elasticsearch:9200"
                index => "%{[@metadata][beat]}-%{[@metadata][version]}-%{[@metadata][tag]}"
                document_id => "%{fingerprint}"
                user => "elastic"
                password => "changeme"
            }
        }
    }

We simply check if tags contain ``json``, then treat it as JSON. If we have
multiple logger producing different JSON data structures, we could change the
``json`` into more detailed (like ``json-document``, ``json-article``, etc).

We want to avoid records duplication. That's why we bind ``id``, ``action``
and ``date`` together into a (temporary) ``raw_id`` field and then run a
fingerprint over it in order to use it as a index document id. Afterwards,
we remove the ``raw_id`` (otherwise it would end up in the index).

Finally, we add tag into metadata, so that in the ``output`` part we could
output data into different Elasticsearch indexes (think of ``json-document``,
``json-article``, etc).
