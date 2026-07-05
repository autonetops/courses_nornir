from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_netmiko.tasks import netmiko_send_command
from nornir_scrapli.tasks import send_command as scrapli_send_command
from nornir_utils.plugins.functions import print_result

import transform  # noqa: F401  (registra "prepara_host" do config.yaml)

nr = InitNornir(config_file="config.yaml")

# Roda so nos roteadores IOS-XE (o F5 e API-only; ver f5_api_lab.py).
roteadores = nr.filter(platform="cisco_xe")

# 1) netmiko — texto CRU (voce faz o parsing).
r_netmiko = roteadores.run(task=netmiko_send_command, command_string="show version")

# 2) napalm — dados ESTRUTURADOS via getters (multi-vendor, sem parsing).
#    Usa a connection_option napalm.platform = "ios".
r_napalm = roteadores.run(task=napalm_get, getters=["facts"])

# 3) scrapli — texto cru, porem rapido e com API moderna.
#    Usa a connection_option scrapli.platform = "cisco_iosxe".
r_scrapli = roteadores.run(task=scrapli_send_command, command="show version")

# 4) o MESMO getter na Arista — outro fabricante, as MESMAS chaves.
#    Usa a connection_option napalm.platform = "eos".
aristas = nr.filter(platform="arista_eos")
r_napalm_eos = aristas.run(task=napalm_get, getters=["facts"])

# napalm ja devolve dict: nada de regex para pegar o modelo —
# e as chaves sao identicas em Cisco e Arista.
print("modelo de r1   (napalm):", r_napalm["r1"].result["facts"]["model"])
print("modelo de eos1 (napalm):", r_napalm_eos["eos1"].result["facts"]["model"])
print("chaves r1  :", sorted(r_napalm["r1"].result["facts"]))
print("chaves eos1:", sorted(r_napalm_eos["eos1"].result["facts"]))
print_result(r_napalm)
print_result(r_napalm_eos)
