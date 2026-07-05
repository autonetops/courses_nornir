from nornir import InitNornir
from nornir_utils.plugins.functions import print_result

from tasks.facts import uptime

import transform  # noqa: F401  (registra "prepara_host" do config.yaml)

nr = InitNornir(config_file="config.yaml")

# So os roteadores IOS-XE falam CLI e entendem "show version | include uptime".
roteadores = nr.filter(platform="cisco_xe")
resultado = roteadores.run(task=uptime)
print_result(resultado)
