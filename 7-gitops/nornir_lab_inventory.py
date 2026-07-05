"""Inventory plugin proprio: o inventario inteiro nasce do CMDB.

Em vez de YAML editado a mao (SimpleInventory), o plugin le o export
inventory/hosts.json e constroi Hosts/Groups/Defaults em Python — o
mesmo mecanismo que o nornir-infrahub usa na Parte II, so que la a
fonte e um Source of Truth de verdade.

Uso (registrar ANTES do InitNornir):
    InventoryPluginRegister.register("LabJSONInventory", LabJSONInventory)
"""

import json
from pathlib import Path

from nornir.core.inventory import (
    ConnectionOptions,
    Defaults,
    Groups,
    Host,
    Hosts,
    Inventory,
)

# O mapeamento por plataforma que no SimpleInventory morava em
# groups.yaml (connection_options) agora e responsabilidade do plugin.
PLATAFORMA_NAPALM = {"cisco_xe": "ios", "arista_eos": "eos"}
PLATAFORMA_SCRAPLI = {"cisco_xe": "cisco_iosxe", "arista_eos": "arista_eos"}


class LabJSONInventory:
    """Constroi o inventario a partir de um export JSON do CMDB."""

    def __init__(self, arquivo: str = "inventory/hosts.json") -> None:
        self.arquivo = Path(arquivo)

    def load(self) -> Inventory:
        dados = json.loads(self.arquivo.read_text())

        hosts = Hosts()
        for nome, attrs in dados.items():
            plataforma = attrs["platform"]
            connection_options = {}
            if plataforma in PLATAFORMA_NAPALM:
                connection_options["napalm"] = ConnectionOptions(
                    platform=PLATAFORMA_NAPALM[plataforma]
                )
            if plataforma in PLATAFORMA_SCRAPLI:
                connection_options["scrapli"] = ConnectionOptions(
                    platform=PLATAFORMA_SCRAPLI[plataforma]
                )
            hosts[nome] = Host(
                name=nome,
                hostname=attrs["ip"],
                platform=plataforma,
                data={k: v for k, v in attrs.items() if k not in ("ip", "platform")},
                connection_options=connection_options,
            )

        return Inventory(hosts=hosts, groups=Groups(), defaults=Defaults())
