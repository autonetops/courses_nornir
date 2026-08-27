from nornir.core.inventory import Host
from nornir.core.processor import Processor
from nornir.core.task import AggregatedResult, MultiResult, Task


class Progress(Processor):
    """Progress processor: a clean report instead of `print_result`.

    A processor gets callbacks at the key moments of the execution. Here we
    accumulate the per-host status in `task_instance_completed` (which fires
    when EACH host finishes) and print an ordered summary at the end.
    """

    def __init__(self) -> None:
        self.status: dict[str, bool] = {}

    def task_started(self, task: Task) -> None:
        total = len(task.nornir.inventory.hosts)
        print(f"=== {task.name}: running on {total} host(s) ===")

    def task_instance_started(self, task: Task, host: Host) -> None:
        pass

    def task_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        self.status[host.name] = not result.failed

    def task_completed(self, task: Task, result: AggregatedResult) -> None:
        for name in sorted(self.status):
            mark = "OK  " if self.status[name] else "FAIL"
            print(f"[{mark}] {name}")
        print(f"=== {len(result.failed_hosts)} failure(s) ===")

    def subtask_instance_started(self, task: Task, host: Host) -> None:
        pass

    def subtask_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        pass
