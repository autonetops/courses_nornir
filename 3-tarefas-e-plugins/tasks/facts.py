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

    Exercise (Aula 1) — complete the TODOs below.
    Full solution: solutions/tasks/facts.py
    """
    # >>> TODO(1): pick the command for THIS host — task.host.platform is the
    #              key into UPTIME_COMMAND.
    # >>> TODO(2): run netmiko_send_command as a SUBTASK via task.run(...),
    #              passing the command as command_string= (and name=command,
    #              so the output block is labeled with it).
    # >>> TODO(3): the subtask's .result is the raw output — keep only the
    #              uptime line (.strip() it).
    # >>> TODO(4): return a Result(host=task.host, result=<the clean line>).
    raise NotImplementedError("complete the TODOs (see solutions/tasks/facts.py)")
