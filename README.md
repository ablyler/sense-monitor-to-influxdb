[![Dockerhub](https://img.shields.io/docker/pulls/ablyler/sense-monitor-to-influxdb)](https://hub.docker.com/repository/docker/ablyler/sense-monitor-to-influxdb/general)

# sense-monitor-to-influxdb

Pull instantaneous electricity usage readings from an Sense Monitor via a Web Socket and ship them to InfluxDB.

## Usage

Here are some example snippets to help you get started creating a container.

### docker-compose (recommended)

```yaml
---
version: "2.1"
  sense_monitor_to_influxdb:
    image: ablyler/sense-monitor-to-influxdb:latest
    environment:
      SENSE_MONITOR_NAME: "geothermal"
      SENSE_USERNAME: "joe@domain.com"
      SENSE_PASSWORD: ""
      INFLUXDB_URL: "http://influxdb:8086"
      INFLUXDB_TOKEN: ""
      INFLUXDB_ORG: "org"
      INFLUXDB_BUCKET: "sense"
    restart: unless-stopped
```

### docker cli

```bash
docker run -d \
  --name=sense_monitor_to_influxdb \
  -e SENSE_MONITOR_NAME="geothermal" \
  -e SENSE_USERNAME="joe@domain.com" \
  -e SENSE_PASSWORD="" \
  -e INFLUXDB_URL="" \
  -e INFLUXDB_TOKEN="" \
  -e INFLUXDB_ORG="" \
  -e INFLUXDB_BUCKET="" \
  --restart unless-stopped \
  ablyler/sense-monitor-to-influxdb:latest
```

## Configuration

* `SENSE_MONITOR_NAME`: Name to use to identify multiple Sense monitors (this can be anything you want it to be)
* `SENSE_USERNAME`: Sense username
* `SENSE_PASSWORD`: Sense password
* `INFLUXDB_URL`: InfluxDB url, including protocol and port,  eg. 'http://192.168.1.1:8086'
* `INFLUXDB_TOKEN`: InfluxDB token
* `INFLUXDB_ORG`: InfluxDB org
* `INFLUXDB_BUCKET`: InfluxDB bucket

## License

MIT; see `LICENSE` in this repository.

## Author

[Andy Blyler](https://andyblyler.com) (GitHub [@ablyler](https://github.com/ablyler)).
