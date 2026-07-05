"""Inicializa o Nornir com inventario vindo do Infrahub.

O InfrahubInventory (pacote nornir-infrahub) e auto-registrado via entry
point — nao ha InventoryPluginRegister.register. O token nunca mora no
YAML: carrega de INFRAHUB_TOKEN e injeta aqui.
"""

import os

import yaml
from nornir import InitNornir

# config-infrahub.yaml traz TODAS as opcoes MENOS o token (segredo fora do Git).
with open("config-infrahub.yaml", encoding="utf-8") as fh:
    cfg = yaml.safe_load(fh)
cfg["inventory"]["options"]["token"] = os.environ["INFRAHUB_TOKEN"]

nr = InitNornir(**cfg)

# Credenciais de device tambem vem de env, aplicadas aos defaults.
nr.inventory.defaults.username = os.environ["NORNIR_USER"]
nr.inventory.defaults.password = os.environ["NORNIR_PASS"]

print(f"{len(nr.inventory.hosts)} hosts vindos do Infrahub:")
for nome, host in sorted(nr.inventory.hosts.items()):
    grupos = ",".join(sorted(g.name for g in host.groups))
    print(f"  {nome:<5} {host.hostname:<16} {host.platform:<11} [{grupos}]")

# um host cisco qualquer, para provar que o connection_options veio do grupo
cisco = nr.filter(platform="cisco_xe")
if not cisco.inventory.hosts:
    raise SystemExit(
        "nenhum host com platform cisco_xe — confira o atributo "
        "nornir_platform no Infrahub"
    )
algum = next(iter(cisco.inventory.hosts.values()))
print("napalm platform:", algum.get_connection_parameters("napalm").platform)
