"""Demonstracao device-free: taxonomia de falhas, retry e exit code.

Simula um host INSTAVEL (r1: falha de conexao nas 2 primeiras vezes),
um host com DADOS quebrados (r3: nenhum retry conserta) e hosts
saudaveis. Roda sem lab — as falhas sao levantadas em Python puro.
"""

import sys

from nornir import InitNornir
from nornir.core.exceptions import NornirSubTaskError
from nornir.core.task import Result, Task

import transform  # noqa: F401  (registra "prepara_host" do config.yaml)

VEZES: dict[str, int] = {}


def coleta_simulada(task: Task) -> Result:
    """Simula a task real: r1 e instavel, r3 tem dado quebrado."""
    vez = VEZES.get(task.host.name, 0) + 1
    VEZES[task.host.name] = vez
    if task.host.name == "r1" and vez < 3:
        raise ConnectionError(f"timeout simulado (vez {vez})")
    if task.host.name == "r3":
        raise ValueError("payload invalido no inventario (simulado)")
    return Result(host=task.host, result=f"coleta OK na vez {vez}")


def coleta_com_retry(task: Task, tentativas: int = 3) -> Result:
    """Retry limitado: so a tentativa final conta no placar."""
    for tentativa in range(1, tentativas):
        marco = len(task.results)
        try:
            r = task.run(task=coleta_simulada, name=f"tentativa {tentativa}")
            return Result(host=task.host, result=r.result)
        except NornirSubTaskError:
            del task.results[marco:]  # descarta a tentativa falha
    # Ultima chance, sem try: se falhar, a falha REAL vai para o placar.
    r = task.run(task=coleta_simulada, name=f"tentativa {tentativas}")
    return Result(host=task.host, result=r.result)


nr = InitNornir(config_file="config.yaml")
roteadores = nr.filter(platform="cisco_xe")
resultado = roteadores.run(task=coleta_com_retry, tentativas=3)

# Relatorio de falha parcial: quem falhou, e POR QUE (taxonomia).
print(f"== relatorio: {len(resultado)} host(s) ==")
for nome in sorted(resultado):
    mr = resultado[nome]
    if mr.failed:
        excecao = mr[-1].exception  # a excecao da ultima tentativa
        print(f"[FALHA] {nome}: {type(excecao).__name__}: {excecao}")
    else:
        print(f"[OK   ] {nome}: {mr.result}")

codigo = 1 if resultado.failed else 0
print(f"exit code: {codigo}")
sys.exit(codigo)
