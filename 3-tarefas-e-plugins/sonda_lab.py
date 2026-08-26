from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result

from tasks.sonda import probe_ports

nr = InitNornir(config_file="config.yaml")

# Only peer-inet-01 — the single host in the inventory without SSH.
# Note: the probe does not even need credentials — it is a plain TCP socket.
no_ssh_hosts = nr.filter(F(no_ssh=True))
results = no_ssh_hosts.run(task=probe_ports)
print_result(results)
