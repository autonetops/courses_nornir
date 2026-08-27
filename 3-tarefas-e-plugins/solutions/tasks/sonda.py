import socket

from nornir.core.task import Result, Task

PORTS = {"ssh": 22, "bgp": 179}


def probe_ports(task: Task, timeout: float = 3.0) -> Result:
    """Probes the host TCP ports — automation with NO CLI and NO API.

    peer-inet-01 (`no_ssh: true` in the inventory) runs no sshd and the FRR
    vtysh only answers inside the container. But a task is just Python: a
    TCP socket answers what actually matters — is the BGP service
    (port 179) up?
    """
    state = {}
    for name, port in PORTS.items():
        try:
            with socket.create_connection((task.host.hostname, port), timeout):
                state[f"{name} ({port})"] = "open"
        except OSError:
            state[f"{name} ({port})"] = "closed"
    return Result(host=task.host, result=state)
