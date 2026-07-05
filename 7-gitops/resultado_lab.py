from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_utils.plugins.functions import print_result

import transform  # noqa: F401  (registra "prepara_host" do config.yaml)
from processors import Progresso


def verifica_ssh(task: Task) -> Result:
    """Simula uma verificacao de acesso (device-free, roda sem lab).

    O F5 e API-only, entao 'falha' no SSH — perfeito para estudar
    hosts que falham, `failed_hosts` e processors sem depender do lab.
    """
    if task.host.get("api_only", False):
        raise ConnectionError("dispositivo API-only nao fala SSH")
    return Result(host=task.host, result=f"{task.host.name}: SSH OK")


nr = InitNornir(config_file="config.yaml")

# 1) Execucao crua: por padrao, uma falha NAO interrompe os demais.
resultado = nr.run(task=verifica_ssh)
print("failed?      ", resultado.failed)
print("failed_hosts ", sorted(resultado.failed_hosts))
print("f5 exception ", repr(resultado["f5"][0].exception))
print()

# 2) Mesmo trabalho, com um processor para um relatorio limpo.
#    nr fresco: senao o f5 (ja marcado como falho) seria PULADO.
nr2 = InitNornir(config_file="config.yaml")
nr2.with_processors([Progresso()]).run(task=verifica_ssh)

# 3) print_result com filtro de severidade: so o que falhou.
import logging  # noqa: E402

print()
print_result(resultado, severity_level=logging.WARNING)
