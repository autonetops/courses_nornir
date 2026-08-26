import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.username = os.environ["NORNIR_USER"]
nr.inventory.defaults.password = os.environ["NORNIR_PASS"]
srl = nr.inventory.groups["srl"]
srl.username = os.environ.get("SRL_USER", os.environ["NORNIR_USER"])
srl.password = os.environ.get("SRL_PASS", os.environ["NORNIR_PASS"])

# "janela de manutencao no POP A": um filtro, tres plataformas —
# pe-emea-01 (Arista EOS), core-rr-01 (Cisco IOL) e ce-custc-01 (SR Linux)
pop_a = nr.filter(F(site="emea-pop-a"))
resultado = pop_a.run(
    task=netmiko_send_command,
    command_string="show version",
)
print_result(resultado)
