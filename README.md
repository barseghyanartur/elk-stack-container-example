# ELK stack
ELK stack (dev) with Docker and Podman

## Usage

```shell-script
podman-compose up
```

## Services

- [Elasticsearch](http://localhost:9200/)
- [Kibana](http://localhost:5601/)
- [Logstash](http://localhost:8080/)

## Add messages to logstash

### From Python (using TCP)

```python
import logging 
import logstash 

host = "localhost"
test_logger = logging.getLogger("my-logger")
test_logger.setLevel(logging.INFO)
test_logger.addHandler(logstash.TCPLogstashHandler(host, 12345, version=1))
test_logger.error("Test error message.")
```

### Using cURL via HTTP

```shell-script
curl --request POST \
  --url http://localhost:8080/ \
  --header 'content-type: application/json' \
  --data '"Test error message."'
```
