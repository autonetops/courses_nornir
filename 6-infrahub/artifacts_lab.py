"""Gera e puxa o artifact 'startup-config' via nornir-infrahub."""

import os

import yaml
from nornir import InitNornir
from nornir_infrahub.plugins.tasks import generate_artifacts, get_artifact
from nornir_utils.plugins.functions import print_result

with open("config-infrahub.yaml", encoding="utf-8") as fh:
    cfg = yaml.safe_load(fh)
cfg["inventory"]["options"]["token"] = os.environ["INFRAHUB_TOKEN"]
nr = InitNornir(**cfg)

routers = nr.filter(platform="cisco_xe")

# Gera a artifact definition UMA vez (nao por host): basta um host disparar.
run_once = nr.filter(name="r1")
run_once.run(task=generate_artifacts, artifact="startup-config", timeout=30)

# Puxa o conteudo renderizado por host.
resultado = routers.run(task=get_artifact, artifact="startup-config")
print_result(resultado)
