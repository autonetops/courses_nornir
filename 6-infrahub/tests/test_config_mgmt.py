"""Testes do workflow de configuracao — napalm_configure e FALSIFICADO.

monkeypatch troca a task de deploy por uma funcao nossa: o teste
verifica o COMPORTAMENTO do workflow (dry-run por padrao, commit
explicito, plataforma sem template, retry) sem nenhum equipamento.
"""

from nornir.core.task import Result

import tasks.config_mgmt as config_mgmt


def test_configurar_e_dry_run_por_padrao(nr, monkeypatch):
    chamadas = []

    def falso_configure(task, configuration, dry_run):
        chamadas.append({"dry_run": dry_run, "configuration": configuration})
        return Result(host=task.host, diff="+config nova", changed=True)

    monkeypatch.setattr(config_mgmt, "napalm_configure", falso_configure)

    r = nr.filter(name="r1").run(task=config_mgmt.configurar)

    assert not r.failed
    assert chamadas[0]["dry_run"] is True            # padrao seguro
    assert "interface Loopback0" in chamadas[0]["configuration"]
    assert r["r1"].result == "+config nova"          # diff no Result de topo
    assert r["r1"].changed is True


def test_configurar_commit_desliga_dry_run(nr, monkeypatch):
    chamadas = []

    def falso_configure(task, configuration, dry_run):
        chamadas.append({"dry_run": dry_run})
        return Result(host=task.host, diff="", changed=False)

    monkeypatch.setattr(config_mgmt, "napalm_configure", falso_configure)

    r = nr.filter(name="r1").run(task=config_mgmt.configurar, commit=True)

    assert not r.failed
    assert chamadas[0]["dry_run"] is False
    assert r["r1"].changed is False  # sem diff, nada a comitar


def test_plataforma_sem_template_falha_com_mensagem(nr):
    r = nr.filter(name="f5").run(task=config_mgmt.configurar)

    assert r.failed
    assert sorted(r.failed_hosts) == ["f5"]
    assert r["f5"][0].result == "plataforma sem template: f5_bigip"


def test_retry_recupera_falha_transitoria(nr, monkeypatch):
    vezes = {"n": 0}

    def configure_instavel(task, configuration, dry_run):
        vezes["n"] += 1
        if vezes["n"] < 2:
            raise ConnectionError("timeout simulado")
        return Result(host=task.host, diff="+ok", changed=True)

    monkeypatch.setattr(config_mgmt, "napalm_configure", configure_instavel)

    r = nr.filter(name="r1").run(
        task=config_mgmt.configurar_com_retry, tentativas=3
    )

    assert not r.failed          # a 2a tentativa salvou o host
    assert vezes["n"] == 2
    assert r["r1"].result == "+ok"
