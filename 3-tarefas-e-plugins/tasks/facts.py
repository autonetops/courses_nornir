from nornir.core.task import Result, Task
from nornir_netmiko.tasks import netmiko_send_command

# Each NOS prints the uptime its own way: IOS has the "... uptime is" line,
# EOS has "Uptime: ...". The task hides that difference from its caller.
UPTIME_COMMAND = {
    "cisco_ios": "show version | include uptime",
    "arista_eos": "show version | include Uptime",
}


def uptime(task: Task) -> Result:
    """Custom task on top of netmiko: collects the uptime line and returns just it.

    Shows the anatomy of a task: it takes `task`, picks the command from the
    host platform, runs a subtask (`netmiko_send_command`) through
    `task.run`, processes the raw output and returns a clean `Result`.
    """
    command = UPTIME_COMMAND[task.host.platform]
    output = task.run(
        task=netmiko_send_command,
        command_string=command,
        name=command,
    )
    line = output.result.strip()
    return Result(host=task.host, result=line)
