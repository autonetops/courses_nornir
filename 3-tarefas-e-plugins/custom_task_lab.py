import os

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result

from tasks.facts import uptime

nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.username = os.environ["NORNIR_USER"]
nr.inventory.defaults.password = os.environ["NORNIR_PASS"]

# So os roteadores IOS-XE falam CLI e entendem "show version | include uptime".
roteadores = nr.filter(platform="cisco_xe")
resultado = roteadores.run(task=uptime)
print_result(resultado)
