import os

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_netmiko.tasks import netmiko_send_command
from nornir_scrapli.tasks import send_command as scrapli_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.username = os.environ["NORNIR_USER"]
nr.inventory.defaults.password = os.environ["NORNIR_PASS"]

# Runs on both Arista PEs (peer-inet-01 does not speak SSH; see sonda_lab.py).
pes = nr.filter(platform="arista_eos")

# 1) netmiko — RAW text (you do the parsing).
r_netmiko = pes.run(
    task=netmiko_send_command, command_string="show version"
)

# 2) napalm — STRUCTURED data through getters (multi-vendor, no parsing).
#    Uses the connection_option napalm.platform = "eos" (eAPI, not SSH).
r_napalm = pes.run(task=napalm_get, getters=["facts"])

# 3) scrapli — raw text too, but fast and with a modern API.
#    Uses the connection_option scrapli.platform = "arista_eos".
r_scrapli = pes.run(
    task=scrapli_send_command, command="show version"
)

# 4) the SAME getter on the Cisco core — another vendor, the SAME keys.
#    Uses the connection_option napalm.platform = "ios".
core = nr.filter(platform="cisco_ios")
r_napalm_ios = core.run(task=napalm_get, getters=["facts"])

# napalm already returns a dict: no regex to grab the model —
# and the keys are identical on Arista and Cisco.
print("pe-emea-01 model (napalm):", r_napalm["pe-emea-01"].result["facts"]["model"])
print("core-rr-01 model (napalm):", r_napalm_ios["core-rr-01"].result["facts"]["model"])
print("pe-emea-01 keys:", sorted(r_napalm["pe-emea-01"].result["facts"]))
print("core-rr-01 keys:", sorted(r_napalm_ios["core-rr-01"].result["facts"]))
print_result(r_napalm)
print_result(r_napalm_ios)
