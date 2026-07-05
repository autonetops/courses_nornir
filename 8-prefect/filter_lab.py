from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

import transform  # noqa: F401  (registra "prepara_host" do config.yaml)

nr = InitNornir(config_file="config.yaml")

# "so os edge de POA": aplica a task so em r1 e eos1
edge_poa = nr.filter(F(role="edge") & F(site="poa"))
resultado = edge_poa.run(
    task=netmiko_send_command,
    command_string="show clock",
)
print_result(resultado)
