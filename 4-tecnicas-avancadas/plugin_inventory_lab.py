"""Carrega o inventario com o plugin proprio (device-free).

Registra o LabJSONInventory, inicializa pelo config_plugin.yaml e
mostra que hosts, dados e connection_options nasceram do hosts.json —
nenhum YAML de inventario foi lido.
"""

from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister

import transform  # noqa: F401  (registra "prepara_host")
from nornir_lab_inventory import LabJSONInventory

# O registro precede o InitNornir — como nas transform functions.
InventoryPluginRegister.register("LabJSONInventory", LabJSONInventory)

nr = InitNornir(config_file="config_plugin.yaml")

for nome, host in sorted(nr.inventory.hosts.items()):
    print(
        f"{nome:<5} {host.hostname:<14} {host.platform:<11}"
        f" site={host['site']} role={host['role']} serial={host['serial']}"
    )

napalm = nr.inventory.hosts["r1"].get_connection_parameters("napalm")
print("napalm platform de r1:", napalm.platform)
print("mgmt_ip de r1 (transform):", nr.inventory.hosts["r1"]["mgmt_ip"])
