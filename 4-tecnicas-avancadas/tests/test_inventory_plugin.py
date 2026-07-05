"""Testes do inventory plugin — a classe e testavel sem registro."""

from pathlib import Path

from nornir_lab_inventory import LabJSONInventory

RAIZ = Path(__file__).parent.parent


def _inventario():
    plugin = LabJSONInventory(arquivo=str(RAIZ / "inventory" / "hosts.json"))
    return plugin.load()


def test_plugin_carrega_os_sete_hosts():
    inv = _inventario()
    assert sorted(inv.hosts) == ["eos1", "eos2", "f5", "r1", "r2", "r3", "r4"]


def test_plugin_mapeia_ip_plataforma_e_dados():
    inv = _inventario()
    r1 = inv.hosts["r1"]
    assert r1.hostname == "172.20.20.11"
    assert r1.platform == "cisco_xe"
    assert r1.data["site"] == "poa"
    assert r1.data["serial"] == "9XORQC1J2P9E"


def test_plugin_define_connection_options_por_plataforma():
    inv = _inventario()
    assert inv.hosts["r1"].connection_options["napalm"].platform == "ios"
    assert inv.hosts["r1"].connection_options["scrapli"].platform == "cisco_iosxe"
    assert inv.hosts["eos1"].connection_options["napalm"].platform == "eos"
    assert "napalm" not in inv.hosts["f5"].connection_options  # API-only
