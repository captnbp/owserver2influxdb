# Docker OWclient -> InfluxDB
This script fetch the temperature from one or many OWservers. It adds some tags using a configuration file.

## Config file 
This config file ```conf.yml``` is used to setup your InfluxDB connection settings and the list of you OWservers with their sensors.
```yaml
interval: 300
influxdb:
  host: 
  port: 8086
  user: 
  password: 
  db: temperature
owservers:
  - region: 
    hostname: yourserverhostname
    owserver_host: 
    owserver_port: 4304
    sensors: 
      - zone: bedroom
        id: /28.XXXXXXXXXXXX
      - zone: kitchen
        id: /28.XXXXXXXXXXXX
      - zone: ext
        id: /28.XXXXXXXXXXXX
```

## Build
```bash
docker build -t temperature .
```
## Run

```bash
docker run -d --name=temperature -v /srv/temperature/etc/conf.yml:/conf.yml:ro temperature
```
