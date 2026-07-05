from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result

import transform  # noqa: F401  (registra "prepara_host" do config.yaml)

nr = InitNornir(config_file="config.yaml")

roteadores = nr.filter(platform="cisco_xe")


# --- Opcao A: netmiko_send_config — envia comandos crus, SEM dry-run/diff ---
# netmiko so digita os comandos e retorna changed=True. Nao ha diff nem
# rollback; passar dry_run=True aqui LEVANTA erro (netmiko nao suporta).
def config_dominio(task: Task) -> Result:
    return task.run(
        task=netmiko_send_config,
        config_commands=["ip domain name nornir.lab"],
        name="netmiko_send_config",
    )


# --- Opcao B: napalm_configure — dry-run, diff e idempotencia ---
# napalm carrega um candidate, calcula o diff e faz ROLLBACK (dry_run=True).
# Rodar de novo apos comitar => diff vazio => changed=False (idempotente).
def config_loopback(task: Task) -> Result:
    config = "\n".join(
        [
            "interface Loopback100",
            f" description gerenciada-pelo-nornir :: {task.host['site']}",
            f" ip address {task.host['loopback_ip']} 255.255.255.255",
        ]
    )
    r = task.run(
        task=napalm_configure,
        configuration=config,
        dry_run=True,  # troque para False para COMITAR de verdade
        name="napalm_configure (dry-run)",
    )
    # r.diff traz o diff; r.changed indica se havia algo a mudar.
    return Result(host=task.host, result=r.diff, changed=r.changed)


resultado = roteadores.run(task=config_loopback)
print_result(resultado)
