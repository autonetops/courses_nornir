"""Flow de deploy: embrulha o workflow do Cap. 4 num @flow com @task.

O `configurar_com_retry` (Cap. 4) ja retenta POR HOST dentro da task Nornir.
Por cima, o Prefect retenta POR TASK: aqui cada SITE e uma task, entao uma
falha em POA retenta so POA — nunca GRU. Sao duas camadas de retry, cada uma
na granularidade certa (o oposto do `retry:` do GitLab, que repete o job
inteiro).

Thread-safety: o `InitNornir` roda DENTRO da task — um objeto Nornir por task
run, nunca compartilhado entre execucoes concorrentes do flow.

    python flows/deploy_flow.py            # dry-run em poa e gru
"""

import os

from nornir import InitNornir
from nornir.core.filter import F
from prefect import flow, task

import transform  # noqa: F401  (registra "prepara_host" do config.yaml)
from tasks.config_mgmt import TEMPLATES_POR_PLATAFORMA, configurar_com_retry


@task(retries=2, retry_delay_seconds=10, log_prints=True)
def deploy_site(site: str, commit: bool, tentativas: int) -> dict:
    """Roda o workflow do Cap. 4 no inventario, filtrado por um site.

    Um `InitNornir` por chamada = um objeto Nornir por task run (thread-safe).
    Se algum host falhar, a task levanta erro e o Prefect aplica `retries`
    — retentando SO este site, nao os outros.
    """
    for var in ("NORNIR_USER", "NORNIR_PASS"):
        if var not in os.environ:
            raise RuntimeError(f"variavel de ambiente {var} nao definida")

    nr = InitNornir(config_file="config.yaml")
    alvo = nr.filter(F(platform__any=sorted(TEMPLATES_POR_PLATAFORMA)))
    alvo = alvo.filter(site=site)
    if not alvo.inventory.hosts:
        raise RuntimeError(f"nenhum host no site {site}")

    modo = "COMMIT" if commit else "dry-run"
    nomes = ", ".join(sorted(alvo.inventory.hosts))
    print(f"[{site}] deploy ({modo}) em {len(alvo.inventory.hosts)} host(s): {nomes}")

    resultado = alvo.run(
        task=configurar_com_retry, commit=commit, tentativas=tentativas
    )
    mudou = sorted(h for h, r in resultado.items() if r.changed)
    if resultado.failed:
        falhos = ", ".join(sorted(resultado.failed_hosts))
        raise RuntimeError(f"[{site}] falha em: {falhos}")
    print(f"[{site}] ok: {len(mudou)} host(s) com mudanca")
    return {"site": site, "hosts": sorted(alvo.inventory.hosts), "changed": mudou}


@flow(name="deploy-config", log_prints=True)
def deploy_config(
    sites: list[str] | None = None, commit: bool = False, tentativas: int = 3
) -> dict:
    """Flow de deploy: uma task por site, cada uma com retry proprio."""
    sites = sites or ["poa", "gru"]
    print(f"== flow deploy-config (sites={sites}, commit={commit})")
    return {site: deploy_site(site, commit, tentativas) for site in sites}


if __name__ == "__main__":
    deploy_config()
