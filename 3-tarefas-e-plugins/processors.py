from nornir.core.inventory import Host
from nornir.core.processor import Processor
from nornir.core.task import AggregatedResult, MultiResult, Task


class Progresso(Processor):
    """Processor de progresso: um relatorio limpo em vez de `print_result`.

    Um processor recebe callbacks nos momentos-chave da execucao. Aqui
    acumulamos o status por host em `task_instance_completed` (que dispara
    quando CADA host termina) e imprimimos um resumo ordenado no fim.
    """

    def __init__(self) -> None:
        self.status: dict[str, bool] = {}

    def task_started(self, task: Task) -> None:
        total = len(task.nornir.inventory.hosts)
        print(f"=== {task.name}: executando em {total} host(s) ===")

    def task_instance_started(self, task: Task, host: Host) -> None:
        pass

    def task_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        self.status[host.name] = not result.failed

    def task_completed(self, task: Task, result: AggregatedResult) -> None:
        for nome in sorted(self.status):
            marca = "OK  " if self.status[nome] else "FALHA"
            print(f"[{marca}] {nome}")
        print(f"=== {len(result.failed_hosts)} falha(s) ===")

    def subtask_instance_started(self, task: Task, host: Host) -> None:
        pass

    def subtask_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        pass
