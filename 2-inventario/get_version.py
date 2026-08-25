import os
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.username = os.environ["NORNIR_USER"]
nr.inventory.defaults.password = os.environ["NORNIR_PASS"]

# O SR Linux sai de fabrica com outra senha (admin/NokiaSrl1!). A camada de
# GRUPO vence os defaults — mesma hierarquia do inventario, agora com creds.
srl = nr.inventory.groups["srl"]
srl.username = os.environ.get("SRL_USER", os.environ["NORNIR_USER"])
srl.password = os.environ.get("SRL_PASS", os.environ["NORNIR_PASS"])

# Sem filtro: tenta os SEIS hosts — e falha no peer-inet-01 (FRR sem SSH).
# E proposital: e o problema que o filter_lab.py resolve.
resultado = nr.run(
    task=netmiko_send_command,
    command_string="show version",
)
print_result(resultado)
