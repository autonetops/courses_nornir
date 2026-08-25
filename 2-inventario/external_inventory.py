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

for name in ("pe-emea-01", "ce-custc-01", "peer-inet-01"):
    h = nr.inventory.hosts[name]
    print(name, h["model"], h["serial"], h["rack"])
# pe-emea-01 cEOSLab SN-EOS-A101 pop-a-r01
# ce-custc-01 7220 IXR-D3L SN-SRL-A301 pop-a-r03
# peer-inet-01 FRR 10.1 SN-FRR-B401 pop-b-r04
