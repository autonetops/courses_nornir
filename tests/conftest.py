"""Fixtures do pytest: um Nornir de mentira, rapido e sem rede.

O inventario vem de tests/fixtures/ (3 hosts fake), o runner e serial
(deterministico) e o logging fica desligado. Nenhum teste conecta em
dispositivo algum.
"""

from pathlib import Path

import pytest
from nornir import InitNornir

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def nr():
    nornir = InitNornir(
        runner={"plugin": "serial"},
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": str(FIXTURES / "hosts.yaml"),
                "group_file": str(FIXTURES / "groups.yaml"),
                "defaults_file": str(FIXTURES / "defaults.yaml"),
            },
        },
        logging={"enabled": False},
    )
    yield nornir
    nornir.close_connections()
