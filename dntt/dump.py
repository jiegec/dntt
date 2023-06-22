import yaml
import re
from pexpect import pxssh
import pexpect
import sys

with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.Loader)
    for switch in config['switches']:
        child = pexpect.spawn(
            f'ssh -oHostKeyAlgorithms=+ssh-rsa,ssh-dss -o KexAlgorithms=+diffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1 {switch["username"]}@{switch["host"]}', encoding='utf-8')
        child.logfile = sys.stdout
        if switch['vendor'] == 'huawei':
            child.expect('Password:')
            child.sendline(switch["password"])
            child.expect('>')
            child.sendline('screen-length 0 temporary')
            child.sendline('display current-configuration')
            child.sendline('quit')
            child.expect('quit')
            output = child.before
            # strip additional content
            output = output[output.find('display current-configuration'):]
            output = "\n".join(output.split("\n")[1:-1])
        elif switch['vendor'] == 'dell':
            child.expect('password:')
            child.sendline(switch["password"])
            child.expect('>')
            child.sendline('en')
            child.sendline('terminal length 0')
            child.sendline('show run')
            child.sendline('exit')
            child.expect('#exit')
            output = child.before
            # strip additional content
            output = output[output.find('show run'):]
            output = "\n".join(output.split("\n")[1:-1])
        elif switch['vendor'] == 'mellanox':
            child.expect('Password:')
            child.sendline(switch["password"])
            child.expect('>')
            child.sendline('en')
            child.sendline('no cli session paging enable')
            child.sendline('show run')
            child.sendline('exit')
            child.expect('# exit')
            output = child.before
            # strip additional content
            output = output[output.find('show run'):]
            output = output[output.find('exit'):]
            output = re.sub('## Generated at .*', '', output)
            output = "\n".join(output.split("\n")[1:-1])
        elif switch['vendor'] == 'cisco':
            child.expect('Password:')
            child.sendline(switch["password"])
            child.expect('#')
            child.sendline('terminal length 0')
            child.sendline('show run')
            child.sendline('exit')
            child.expect('# exit')
            output = child.before
            # strip additional content
            output = output[output.find('!Command: show running-config'):]
            output = re.sub('!Time: .*', '', output)
            output = "\n".join(output.split("\n")[1:-1])
        else:
            continue
        child.close()

        with open(f'{switch["host"]}.config', 'w') as cfg:
            cfg.write(output)
