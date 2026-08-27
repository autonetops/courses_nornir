import os

from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_jinja2.plugins.tasks import template_file
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.username = os.environ["NORNIR_USER"]
nr.inventory.defaults.password = os.environ["NORNIR_PASS"]


def render_and_deploy(task: Task, path: str) -> Result:
    """Renders the host template and pushes it through NAPALM in dry-run.

    Step 1 (local): template_file builds the config from the host data.
    Step 2 (device): napalm_configure loads it, computes the diff and rolls back.
    Switch dry_run to False to commit.
    """
    render = task.run(
        task=template_file, template="base.j2", path=path, name="render"
    )
    task.run(
        task=napalm_configure,
        configuration=render.result,
        dry_run=True,
        name="deploy (dry-run)",
    )
    return Result(host=task.host, result="ok")


# One pass per platform: each one uses its own template directory.
eos = nr.filter(platform="arista_eos")
r_eos = eos.run(task=render_and_deploy, path="templates/eos")

ios = nr.filter(platform="cisco_ios")
r_ios = ios.run(task=render_and_deploy, path="templates/ios")

print_result(r_eos)
print_result(r_ios)
