"""Workflow de configuracao reutilizavel: render -> diff -> deploy.

Uma unica grouped task cobre todas as plataformas com template: o mapa
TEMPLATES_POR_PLATAFORMA escolhe o diretorio certo, o napalm_configure
calcula o diff e o parametro `commit` decide se e simulacao (dry-run)
ou deploy de verdade.
"""

from pathlib import Path

from nornir.core.exceptions import NornirSubTaskError
from nornir.core.task import Result, Task
from nornir_jinja2.plugins.tasks import template_file
from nornir_napalm.plugins.tasks import napalm_configure

# Caminhos absolutos: o workflow funciona de qualquer cwd (pytest, CI).
_RAIZ = Path(__file__).resolve().parent.parent

TEMPLATES_POR_PLATAFORMA = {
    "cisco_xe": str(_RAIZ / "templates" / "ios"),
    "arista_eos": str(_RAIZ / "templates" / "eos"),
}


def configurar(task: Task, commit: bool = False) -> Result:
    """Renderiza o template da plataforma do host e aplica via NAPALM.

    commit=False (padrao): dry-run — calcula o diff e faz rollback.
    commit=True: comita, se (e somente se) houver diff.
    O Result de topo carrega o diff e o changed do deploy.
    """
    path = TEMPLATES_POR_PLATAFORMA.get(task.host.platform)
    if path is None:
        # Falha de DADOS: plataforma sem template. Nao ha o que retentar.
        return Result(
            host=task.host,
            result=f"plataforma sem template: {task.host.platform}",
            failed=True,
        )
    render = task.run(
        task=template_file, template="base.j2", path=path, name="render"
    )
    deploy = task.run(
        task=napalm_configure,
        configuration=render.result,
        dry_run=not commit,
        name="deploy" if commit else "deploy (dry-run)",
    )
    return Result(host=task.host, result=deploy.diff, changed=deploy.changed)


def configurar_com_retry(
    task: Task, commit: bool = False, tentativas: int = 1
) -> Result:
    """Reexecuta `configurar` ate `tentativas` vezes (retry limitado).

    Tentativas falhas intermediarias sao descartadas do placar
    (del task.results[marco:]); so a tentativa final conta. Se a ultima
    tambem falhar, a falha REAL sobe para o relatorio.
    """
    for tentativa in range(1, tentativas):
        marco = len(task.results)
        try:
            r = task.run(
                task=configurar, commit=commit, name=f"tentativa {tentativa}"
            )
            return Result(host=task.host, result=r.result, changed=r.changed)
        except NornirSubTaskError:
            del task.results[marco:]  # descarta a tentativa falha
    # Ultima chance, sem try: se falhar, a falha aparece no placar.
    r = task.run(
        task=configurar, commit=commit, name=f"tentativa {tentativas}"
    )
    return Result(host=task.host, result=r.result, changed=r.changed)
