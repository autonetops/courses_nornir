"""Inventario nascido do NetBox (plugin NetBoxInventory2).

Device-free: apenas carrega e imprime o inventario. O token nunca mora
em arquivo — exporte NB_URL e NB_TOKEN antes de rodar.
"""

import os

from nornir import InitNornir
from nornir.core.inventory import Host
from nornir.core.plugins.inventory import TransformFunctionRegister

# O NetBox guarda *slugs* de plataforma (eos, ios, srlinux) — nomes do
# NetBox, nao do netmiko. A transform function da aula anterior fecha o
# ciclo: traduz o slug para o nome que o plugin de conexao espera.
PLATFORM_MAP = {
    "eos": "arista_eos",
    "ios": "cisco_ios",
    "srlinux": "nokia_srl",
}


def netbox_para_netmiko(host: Host) -> None:
    host.platform = PLATFORM_MAP.get(host.platform, host.platform)


TransformFunctionRegister.register("netbox_para_netmiko", netbox_para_netmiko)

nr = InitNornir(
    runner={"plugin": "threaded", "options": {"num_workers": 20}},
    inventory={
        # auto-registrado pelo pacote nornir-netbox (entry point)
        "plugin": "NetBoxInventory2",
        "options": {
            "nb_url": os.environ["NB_URL"],
            "nb_token": os.environ["NB_TOKEN"],
            # o NetBox do curso tem outros labs — filtra so o nosso site
            "filter_parameters": {"site": "autonetops_ibn"},
            "use_platform_slug": True,
        },
        "transform_function": "netbox_para_netmiko",
    },
)

print(f"{len(nr.inventory.hosts)} hosts vindos do NetBox:")
for name, host in nr.inventory.hosts.items():
    role = host.data["role"]["slug"]
    model = host.data["device_type"]["model"]
    print(f"  {name:<12} {host.hostname:<14} platform={host.platform:<11} role={role:<10} model={model}")
# 5 hosts vindos do NetBox:
#   CE-CUSTC-01  172.20.20.21   platform=nokia_srl   role=unknown    model=7220-ixr-d3l
#   CE-CUSTC-02  172.20.20.22   platform=nokia_srl   role=unknown    model=7220-ixr-d3l
#   CORE-RR-01   172.20.20.13   platform=cisco_ios   role=rr         model=cisco-generic
#   PE-EMEA-01   172.20.20.11   platform=arista_eos  role=pe-router  model=ceos
#   PE-EMEA-02   172.20.20.12   platform=arista_eos  role=pe-router  model=ceos
