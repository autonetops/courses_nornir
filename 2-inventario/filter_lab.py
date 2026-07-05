import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.username = os.environ["NORNIR_USER"]
nr.inventory.defaults.password = os.environ["NORNIR_PASS"]

# "so os edge de POA": aplica a task so em r1 e eos1
edge_poa = nr.filter(F(role="edge") & F(site="poa"))
resultado = edge_poa.run(
    task=netmiko_send_command,
    command_string="show clock",
)
print_result(resultado)
