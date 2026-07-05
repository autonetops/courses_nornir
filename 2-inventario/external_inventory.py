from nornir import InitNornir
from nornir.core.plugins.inventory import TransformFunctionRegister

from transform import enrich_from_cmdb

TransformFunctionRegister.register("enrich_from_cmdb", enrich_from_cmdb)

nr = InitNornir(
    runner={"plugin": "threaded", "options": {"num_workers": 20}},
    inventory={
        "plugin": "SimpleInventory",
        "options": {
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml",
            "defaults_file": "inventory/defaults.yaml",
        },
        "transform_function": "enrich_from_cmdb",
    },
)

for name in ("r1", "eos1", "f5"):
    h = nr.inventory.hosts[name]
    print(name, h["model"], h["serial"], h["rack"])
# r1 C8000V 9XORQC1J2P9E poa-a01
# eos1 cEOSLab SN-EOS-0001 poa-a03
# f5 BIG-IP-VE SN-F5-0001 poa-a04
