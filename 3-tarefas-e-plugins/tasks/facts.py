from nornir.core.task import Result, Task
from nornir_netmiko.tasks import netmiko_send_command


def uptime(task: Task) -> Result:
    """Task custom sobre netmiko: coleta a linha de uptime e devolve so ela.

    Mostra a anatomia de uma task: recebe `task`, roda uma subtask
    (`netmiko_send_command`) via `task.run`, processa a saida crua e
    devolve um `Result` limpo.
    """
    saida = task.run(
        task=netmiko_send_command,
        command_string="show version | include uptime",
        name="show version | include uptime",
    )
    linha = saida.result.strip()
    return Result(host=task.host, result=linha)
