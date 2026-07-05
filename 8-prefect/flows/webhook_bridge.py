"""Ponte webhook -> Prefect REST: dispara um flow run a partir de um evento.

Quando um proposed change e fundido, o Infrahub dispara um webhook. O caminho
honesto no servidor OSS do Prefect (sem a feature de webhooks do Prefect Cloud)
e um POST no endpoint REST de deployment:

    POST {PREFECT_API_URL}/deployments/{deployment_id}/create_flow_run

O corpo aceita `parameters` (mesclados com os defaults do deployment); o estado
inicial vira `Scheduled` no servidor. Um relay como este traduz o payload do
Infrahub e chama esse endpoint — util quando o webhook do Infrahub nao consegue
montar o corpo exato que o Prefect espera.

    PREFECT_API_URL=http://10.0.0.2:4200/api \
      python flows/webhook_bridge.py <deployment_id>
"""

import os
import sys

import httpx


def disparar_run(deployment_id: str, parametros: dict | None = None) -> str:
    """POST em /deployments/{id}/create_flow_run; devolve o id do flow run."""
    api = os.environ.get("PREFECT_API_URL", "http://10.0.0.2:4200/api")
    url = f"{api}/deployments/{deployment_id}/create_flow_run"
    corpo = {"parameters": parametros or {}}
    resp = httpx.post(url, json=corpo, timeout=30)
    resp.raise_for_status()
    run = resp.json()
    print(f"flow run criado: {run['name']} (id={run['id']})")
    return run["id"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("uso: python flows/webhook_bridge.py <deployment_id>", file=sys.stderr)
        raise SystemExit(2)
    # Parametro do deployment `deploy-config` (Aula 3): so o site POA.
    disparar_run(sys.argv[1], {"sites": ["poa"]})
