#!/usr/bin/env python
from pyownet import protocol
from influxdb import InfluxDBClient
import os
import sys
import yaml
import time

def get_config():
    """ Reads the configuration file """
    try:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        config_file = os.path.join(base_dir, "conf.yml")
        stream = open(config_file, 'r')
    except FileNotFoundError as err:
        print('Cannot find config file {} : {}'.format(config_file, err), file=sys.stderr)
        sys.exit(1)
    except IOError as err:
        print('Cannot read config file {} : {}'.format(config_file, err), file=sys.stderr)
        sys.exit(1)
    try:
        config = yaml.safe_load(stream)
        stream.close()
    except yaml.YAMLError as err:
        if hasattr(err, 'problem_mark'):
            mark = err.problem_mark
            print("Error position in YAML configuration file {}: ({}:{})".format(config_file, mark.line + 1,
                                                                                 mark.column + 1))
            sys.exit(1)
        else:
            print(
                "Error in YAML configuration file {} : {}".format(
                    config_file, err), file=sys.stderr
            )
            sys.exit(1)
    return config



def main():
    config = get_config()
    client = InfluxDBClient(config['influxdb']['host'],
                            config['influxdb']['port'],
                            config['influxdb']['user'],
                            config['influxdb']['password'],
                            config['influxdb']['db']
                            )

    while True:
        for owserver in config['owservers']:
            try:
                proxy = protocol.proxy(owserver['owserver_host'],
                                    owserver['owserver_port'])
            except (protocol.ConnError, protocol.ProtocolError) as err:
                print(err)
                continue

            data = []

            #for sensor in proxy.dir(slash=False, bus=False):
            for sensor in owserver['sensors']:
                stype = proxy.read(sensor['id'] + '/type').decode()
                try:
                    temp = float(proxy.read(sensor['id'] + '/temperature'))
                    measure = { "measurement": "temperature",
                                "tags": {
                                    "region": owserver['region'],
                                    "host": owserver['hostname'],
                                    "zone": sensor['zone'],
                                    "type": stype
                                },
                            "fields": {
                                "value": temp
                            }
                            }
                    print(measure)
                    temp = "{0:.2f}".format(temp)
                    data.append(measure)
                except protocol.OwnetError:
                    temp = ''
            client.write_points(data)
        time.sleep(300)


if __name__ == '__main__':
    main()

