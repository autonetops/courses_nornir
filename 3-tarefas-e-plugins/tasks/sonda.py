import socket

from nornir.core.task import Result, Task

PORTS = {"ssh": 22, "bgp": 179}


def probe_ports(task: Task, timeout: float = 3.0) -> Result:
    """Probes the host TCP ports — automation with NO CLI and NO API.

    peer-inet-01 (`no_ssh: true` in the inventory) runs no sshd and the FRR
    vtysh only answers inside the container. But a task is just Python: a
    TCP socket answers what actually matters — is the BGP service
    (port 179) up?

    Exercise (Aula 2) — complete the TODOs below.
    Full solution: solutions/tasks/sonda.py
    """
    state = {}
    # >>> TODO(1): for each (name, port) in PORTS.items(), try
    #              socket.create_connection((task.host.hostname, port), timeout)
    #              in a `with` block — it returns a socket when the port
    #              answers and raises OSError when it does not.
    # >>> TODO(2): record state[f"{name} ({port})"] = "open" or "closed".
    # >>> TODO(3): return a Result carrying the state dict.
    raise NotImplementedError("complete the TODOs (see solutions/tasks/sonda.py)")
