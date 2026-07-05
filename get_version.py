from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

import transform  # noqa: F401  (registra "prepara_host" do config.yaml)

nr = InitNornir(config_file="config.yaml")

resultado = nr.run(
    task=netmiko_send_command,
    command_string="show version",
)
print_result(resultado)
