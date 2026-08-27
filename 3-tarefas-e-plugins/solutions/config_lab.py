import os

from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.username = os.environ["NORNIR_USER"]
nr.inventory.defaults.password = os.environ["NORNIR_PASS"]

core = nr.filter(platform="cisco_ios")   # core-rr-01
pes = nr.filter(platform="arista_eos")   # pe-emea-01 and pe-emea-02


# --- Option A: netmiko_send_config — sends raw commands, NO dry-run/diff ---
# netmiko only types the commands and returns changed=True. There is no diff
# and no rollback; passing dry_run=True here RAISES an error (unsupported).
# Run it TWICE: changed=True both times — it does not compare, it just types.
def config_domain(task: Task) -> Result:
    return task.run(
        task=netmiko_send_config,
        config_commands=[f"ip domain name {task.host['domain']}"],
        name="netmiko_send_config",
    )


# --- Option B: napalm_configure — dry-run, diff and idempotency ---
# napalm loads a candidate, computes the diff and does a ROLLBACK (dry_run=True).
# Running it again after the commit => empty diff => changed=False (idempotent).
# Loopback0 belongs to the SoT — YOUR study interface is Loopback100.
def config_loopback(task: Task) -> Result:
    config = "\n".join(
        [
            "interface Loopback100",
            f"   description managed-by-nornir :: {task.host['site']}",
            f"   ip address {task.host['lab_loopback']}/32",
        ]
    )
    r = task.run(
        task=napalm_configure,
        configuration=config,
        dry_run=True,  # switch to False to actually COMMIT
        name="napalm_configure (dry-run)",
    )
    # r.diff carries the diff; r.changed says whether there was anything to change.
    return Result(host=task.host, result=r.diff, changed=r.changed)


r_domain = core.run(task=config_domain)
print_result(r_domain)

results = pes.run(task=config_loopback)
print_result(results)
