"""Testes da transform function — chamada direta, sem InitNornir."""

from nornir.core.inventory import Host

from transform import prepara_host


def test_prepara_host_injeta_credenciais_do_env(monkeypatch):
    monkeypatch.setenv("NORNIR_USER", "student")
    monkeypatch.setenv("NORNIR_PASS", "autonetops123")
    host = Host(name="r1", hostname="172.20.20.11")

    prepara_host(host)

    assert host.username == "student"
    assert host.password == "autonetops123"


def test_prepara_host_sem_env_nao_quebra(monkeypatch):
    monkeypatch.delenv("NORNIR_USER", raising=False)
    monkeypatch.delenv("NORNIR_PASS", raising=False)
    host = Host(name="r1", hostname="172.20.20.11")

    prepara_host(host)  # device-free: rodar sem credenciais e valido

    assert host.username is None
    assert host.password is None


def test_prepara_host_enriquece_cmdb_e_derivados(monkeypatch):
    monkeypatch.delenv("NORNIR_USER", raising=False)
    monkeypatch.delenv("NORNIR_PASS", raising=False)
    host = Host(name="r1", hostname="172.20.20.11", data={"site": "poa"})

    prepara_host(host)

    assert host.data["model"] == "C8000V"  # CMDB (hosts.json)
    assert host.data["serial"] == "9XORQC1J2P9E"
    assert host.data["mgmt_ip"] == "10.99.0.11"  # derivado do hostname
    assert host.data["ntp"] == "10.10.0.1"  # servico do site poa
    assert host.data["dns"] == "10.10.0.53"


def test_prepara_host_ignora_host_fora_do_cmdb(monkeypatch):
    monkeypatch.delenv("NORNIR_USER", raising=False)
    monkeypatch.delenv("NORNIR_PASS", raising=False)
    host = Host(name="desconhecido", hostname="192.0.2.99")

    prepara_host(host)

    assert "model" not in host.data
    assert host.data["mgmt_ip"] == "10.99.0.99"
