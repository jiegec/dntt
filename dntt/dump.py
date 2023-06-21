import yaml
import re
from telnetlib import Telnet

with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.Loader)
    for switch in config['switches']:
        with Telnet(switch['host']) as tn:
            if switch['vendor'] == 'huawei':
                tn.write(f'{switch["username"]}\n'.encode('utf-8'))
                tn.write(f'{switch["password"]}\n'.encode('utf-8'))
                tn.write(f'screen-length 0 temporary\n'.encode('utf-8'))
                tn.write(f'display current-configuration\n'.encode('utf-8'))
                tn.write(f'quit\n'.encode('utf-8'))
            output = tn.read_until('quit'.encode('utf-8')).decode('utf-8')
            # strip additional content
            output = output[output.find('display current-configuration'):]
            output = "\n".join(output.split("\n")[1:-1])

            with open(f'{switch["host"]}.config', 'w') as cfg:
                cfg.write(output)
