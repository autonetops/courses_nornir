"""Flow de conformidade agendado: o drift do Cap. 6/7 como deployment cron.

Embrulha o `detectar_drift` (intended do SoT x running do device) num @flow e
serve o flow como um deployment agendado com `.serve(cron=...)`. O agendamento
e o runtime vivem no processo que roda o `.serve` — sem runner efemero, sem
docker-in-docker. E o schedule do GitLab (Cap. 7), mas com estado, retry e
observabilidade.

    # dispara uma execucao agora
    python flows/compliance.py

    # serve como deployment agendado (06:00 todo dia); precisa de
    # PREFECT_API_URL=http://10.0.0.2:4200/api
    python flows/compliance.py --serve
"""

import os
import sys

import yaml
from nornir import InitNornir
from prefect import flow, task

from drift import detectar_drift


@task(retries=2, retry_delay_seconds=30, log_prints=True)
def checar_drift() -> dict:
    """Roda a deteccao de drift nos routers e resume quem divergiu."""
    with open("config-infrahub.yaml", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    cfg["inventory"]["options"]["token"] = os.environ["INFRAHUB_TOKEN"]
    nr = InitNornir(**cfg)
    nr.inventory.defaults.username = os.environ["NORNIR_USER"]
    nr.inventory.defaults.password = os.environ["NORNIR_PASS"]

    routers = nr.filter(platform="cisco_xe")
    resultado = routers.run(task=detectar_drift)
    com_drift = sorted(h for h, r in resultado.items() if r.changed)
    for host in com_drift:
        print(f"DRIFT em {host}")
    if not com_drift:
        print("sem drift em nenhum host")
    return {"com_drift": com_drift, "total": len(resultado)}


@flow(name="compliance-diario", log_prints=True)
def compliance() -> dict:
    """Auditoria diaria: compara o intended (SoT) com o running (device)."""
    print("== flow compliance-diario: auditando intended x running")
    return checar_drift()


if __name__ == "__main__":
    if "--serve" in sys.argv:
        # Deployment agendado: 06:00 todo dia. O processo fica de pe servindo.
        compliance.serve(name="compliance-diario", cron="0 6 * * *")
    else:
        compliance()
