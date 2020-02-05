# ELK stack
ELK stack (dev) with Docker (or Podman)

## Usage

**Using Docker**

```shell-script
docker-compose up
```

**Using Podman**

```shell-script
podman-compose up
```

## Services

- [Elasticsearch](http://localhost:9200/)
- [Kibana](http://localhost:5601/)
- Logstash
- Filebeat

## Add messages to Logstash

**Install requirements**

```shell script
pip install -r requirements.txt
```

**Generate some logs**

```shell script
python factories/generate.py --amount=30000
```
