"""Inventario nascido do Infrahub (plugin InfrahubInventory).

Device-free: apenas carrega e imprime o inventario. O token nunca mora
em arquivo — exporte INFRAHUB_ADDRESS e INFRAHUB_TOKEN antes de rodar.

Repare: nenhuma transform function. O Infrahub modela *como conectar*
(platform.netmiko_device_type) junto com o resto da rede — o schema_mapping
so aponta de onde vem cada atributo do host.
"""

import os

from nornir import InitNornir

nr = InitNornir(
    runner={"plugin": "threaded", "options": {"num_workers": 20}},
    inventory={
        # auto-registrado pelo pacote nornir-infrahub (entry point)
        "plugin": "InfrahubInventory",
        "options": {
            "address": os.environ["INFRAHUB_ADDRESS"],
            "token": os.environ["INFRAHUB_TOKEN"],
            "branch": "main",
            "host_node": {"kind": "DcimDevice"},
            "schema_mappings": [
                {"name": "hostname", "mapping": "primary_address.address"},
                {"name": "platform", "mapping": "platform.netmiko_device_type"},
            ],
            "group_mappings": ["role"],
        },
    },
)

print(f"{len(nr.inventory.hosts)} hosts vindos do Infrahub:")
for name, host in sorted(nr.inventory.hosts.items()):
    grupos = ",".join(sorted(g.name for g in host.groups))
    print(f"  {name:<13} {host.hostname:<14} platform={host.platform:<11} [{grupos}]")
# 7 hosts vindos do Infrahub:
#   ce-custc-01   172.20.20.21   platform=nokia_srl   [monitored_devices,network_devices,role__cpe]
#   ce-custc-02   172.20.20.22   platform=nokia_srl   [monitored_devices,network_devices,role__cpe]
#   core-rr-01    172.20.20.13   platform=cisco_ios   [monitored_devices,network_devices,role__core]
#   oob-sw-01     172.20.20.41   platform=linux       [network_devices,oob_switches,role__tor]
#   pe-emea-01    172.20.20.11   platform=arista_eos  [monitored_devices,network_devices,role__edge]
#   pe-emea-02    172.20.20.12   platform=arista_eos  [monitored_devices,network_devices,role__edge]
#   peer-inet-01  172.20.20.31   platform=linux       [monitored_devices,network_devices,role__edge]
