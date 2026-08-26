import os

from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result

from tasks.facts import uptime

nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.username = os.environ["NORNIR_USER"]
nr.inventory.defaults.password = os.environ["NORNIR_PASS"]

# Arista PEs + Cisco core: the two platforms the uptime task knows about.
# (SR Linux filters with "| grep", not "| include", and the FRR peer has no
# SSH at all — both stay out of this task.)
target = nr.filter(F(platform__any=["arista_eos", "cisco_ios"]))
results = target.run(task=uptime)
print_result(results)
