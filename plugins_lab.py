import os

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_netmiko.tasks import netmiko_send_command
from nornir_scrapli.tasks import send_command as scrapli_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.username = os.environ["NORNIR_USER"]
nr.inventory.defaults.password = os.environ["NORNIR_PASS"]

# Roda so nos roteadores IOS-XE (o F5 e API-only; ver f5_api_lab.py).
roteadores = nr.filter(platform="cisco_xe")

# 1) netmiko — texto CRU (voce faz o parsing).
r_netmiko = roteadores.run(
    task=netmiko_send_command, command_string="show version"
)

# 2) napalm — dados ESTRUTURADOS via getters (multi-vendor, sem parsing).
#    Usa a connection_option napalm.platform = "ios".
r_napalm = roteadores.run(task=napalm_get, getters=["facts"])

# 3) scrapli — texto cru, porem rapido e com API moderna.
#    Usa a connection_option scrapli.platform = "cisco_iosxe".
r_scrapli = roteadores.run(
    task=scrapli_send_command, command="show version"
)

# napalm ja devolve dict: nada de regex para pegar o modelo.
print("modelo de r1 (napalm):", r_napalm["r1"].result["facts"]["model"])
print_result(r_napalm)
