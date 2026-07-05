"""Deteccao de drift: intended (artifact do SoT) x running (napalm)."""

import difflib
import os

import yaml
from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_infrahub.plugins.tasks import get_artifact
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result


def _normaliza(config: str) -> list[str]:
    linhas = []
    for linha in config.splitlines():
        s = linha.rstrip()
        if not s or s.startswith("!"):
            continue
        if s.startswith(("Building configuration", "Current configuration")):
            continue
        linhas.append(s)
    return linhas


def detectar_drift(task: Task) -> Result:
    intended = task.run(task=get_artifact, artifact="startup-config").result
    saida = task.run(task=napalm_get, getters=["config"]).result
    running = saida["config"]["running"]

    diff = list(
        difflib.unified_diff(
            _normaliza(intended),
            _normaliza(running),
            fromfile="intended (SoT)",
            tofile="running (device)",
            lineterm="",
        )
    )
    return Result(
        host=task.host,
        result="\n".join(diff) if diff else "sem drift",
        changed=bool(diff),
        failed=False,
    )


def main() -> int:
    with open("config-infrahub.yaml", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    cfg["inventory"]["options"]["token"] = os.environ["INFRAHUB_TOKEN"]
    nr = InitNornir(**cfg)
    nr.inventory.defaults.username = os.environ["NORNIR_USER"]
    nr.inventory.defaults.password = os.environ["NORNIR_PASS"]

    routers = nr.filter(platform="cisco_xe")
    resultado = routers.run(task=detectar_drift)
    print_result(resultado)
    return 1 if any(h.changed for h in resultado.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
