import os

from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_jinja2.plugins.tasks import template_file
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.username = os.environ["NORNIR_USER"]
nr.inventory.defaults.password = os.environ["NORNIR_PASS"]


def render_e_deploy(task: Task, path: str) -> Result:
    """Renderiza o template do host e envia via NAPALM em dry-run.

    Passo 1 (local): template_file gera a config a partir dos dados do host.
    Passo 2 (device): napalm_configure carrega, calcula o diff e faz rollback.
    Troque dry_run para False para comitar.
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


# Uma passada por plataforma: cada uma usa o seu diretorio de templates.
ios = nr.filter(platform="cisco_xe")
r_ios = ios.run(task=render_e_deploy, path="templates/ios")

eos = nr.filter(platform="arista_eos")
r_eos = eos.run(task=render_e_deploy, path="templates/eos")

print_result(r_ios)
print_result(r_eos)
