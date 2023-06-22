import yaml
import re
from telnetlib import Telnet

with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.Loader)
    for switch in config['switches']:
        with Telnet(switch['host']) as tn:
            tn.set_debuglevel(100)
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
            elif switch['vendor'] == 'dell':
                tn.write(f'{switch["username"]}\n'.encode('utf-8'))
                tn.read_until(f'Password:'.encode('utf-8'))
                tn.write(f'{switch["password"]}\n'.encode('utf-8'))
                tn.write(f'en\n'.encode('utf-8'))
                tn.write(f'terminal length 0\n'.encode('utf-8'))
                tn.write(f'show run\n'.encode('utf-8'))
                tn.write(f'exit\n'.encode('utf-8'))
                output = tn.read_until('#exit'.encode('utf-8')).decode('utf-8')
                # strip additional content
                output = output[output.find('show run'):]
                output = "\n".join(output.split("\n")[1:-1])
            elif switch['vendor'] == 'mellanox':
                tn.read_until(f'login:'.encode('utf-8'))
                tn.write(f'{switch["username"]}\n'.encode('utf-8'))
                tn.read_until(f'Password:'.encode('utf-8'))
                tn.write(f'{switch["password"]}\n'.encode('utf-8'))
                tn.write(f'en\n'.encode('utf-8'))
                tn.write(f'no cli session paging enable\n'.encode('utf-8'))
                tn.write(f'show run\n'.encode('utf-8'))
                tn.write(f'exit\n'.encode('utf-8'))
                output = tn.read_until('# exit'.encode('utf-8')).decode('utf-8')
                # strip additional content
                output = output[output.find('show run'):]
                output = "\n".join(output.split("\n")[1:-1])
            elif switch['vendor'] == 'cisco':
                tn.read_until(f'login:'.encode('utf-8'))
                tn.write(f'{switch["username"]}\n'.encode('utf-8'))
                tn.read_until(f'Password:'.encode('utf-8'))
                tn.write(f'{switch["password"]}\n'.encode('utf-8'))
                tn.write(f'terminal length 0\n'.encode('utf-8'))
                tn.write(f'show run\n'.encode('utf-8'))
                tn.write(f'exit\n'.encode('utf-8'))
                output = tn.read_until('# exit'.encode('utf-8')).decode('utf-8')
                # strip additional content
                output = output[output.find('show run'):]
                output = "\n".join(output.split("\n")[1:-1])
            else:
                continue

            with open(f'{switch["host"]}.config', 'w') as cfg:
                cfg.write(output)
