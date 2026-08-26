from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_utils.plugins.functions import print_result

from processors import Progress


def check_ssh(task: Task) -> Result:
    """Simulates an access check (device-free, runs without the lab).

    peer-inet-01 is `no_ssh: true`, so it 'fails' on SSH — perfect to study
    failing hosts, `failed_hosts` and processors without depending on the lab.
    """
    if task.host.get("no_ssh", False):
        raise ConnectionError("device without SSH — managed through local vtysh")
    return Result(host=task.host, result=f"{task.host.name}: SSH OK")


nr = InitNornir(config_file="config.yaml")

# 1) Raw execution: by default, one failure does NOT stop the others.
results = nr.run(task=check_ssh)
print("failed?      ", results.failed)
print("failed_hosts ", sorted(results.failed_hosts))
print("peer exception", repr(results["peer-inet-01"][0].exception))
print()

# 2) Same work, with a processor for a clean report.
#    A fresh nr: otherwise peer-inet-01 (already marked failed) would be SKIPPED.
nr2 = InitNornir(config_file="config.yaml")
nr2.with_processors([Progress()]).run(task=check_ssh)

# 3) print_result with a severity filter: only what failed.
import logging  # noqa: E402

print()
print_result(results, severity_level=logging.WARNING)
