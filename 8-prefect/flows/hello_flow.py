"""Primeiro flow do Prefect: @flow, @task, retries e log_prints.

Roda 100% local, sem device e sem servidor: o Prefect sobe um servidor
temporario, executa o flow e devolve o valor. E o "hello world" da
orquestracao — a base para embrulhar o deploy e o drift nas proximas aulas.

    python flows/hello_flow.py
"""

from prefect import flow, task


@task(retries=2, retry_delay_seconds=5, log_prints=True)
def dobrar(n: int) -> int:
    """Task simples: dobra um numero. `retries=2` = ate 2 novas tentativas."""
    print(f"dobrando {n}")
    return n * 2


@flow(name="primeiro-flow", log_prints=True)
def principal(n: int = 21) -> int:
    """Flow que chama a task uma vez. log_prints manda os print() pro log."""
    print(f"entrada: {n}")
    r = dobrar(n)
    print(f"saida: {r}")
    return r


if __name__ == "__main__":
    print("return =", principal())
