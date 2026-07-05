"""Testes de inventario e filtros — logica pura, zero conexao."""

from nornir.core.filter import F


def test_inventario_fake_carrega_todos_os_hosts(nr):
    assert sorted(nr.inventory.hosts) == ["eos1", "f5", "r1"]


def test_heranca_de_defaults_e_grupos(nr):
    r1 = nr.inventory.hosts["r1"]
    assert r1["domain"] == "nornir.lab"  # defaults
    assert r1["site"] == "poa"  # grupo site_poa
    assert r1.platform == "cisco_xe"  # grupo ios


def test_filtro_composto_edge_de_poa(nr):
    fatia = nr.filter(F(role="edge") & F(site="poa"))
    assert sorted(fatia.inventory.hosts) == ["eos1", "r1"]


def test_filtro_exclui_api_only(nr):
    sem_api = nr.filter(~F(platform="f5_bigip"))
    assert "f5" not in sem_api.inventory.hosts
    assert sorted(sem_api.inventory.hosts) == ["eos1", "r1"]
