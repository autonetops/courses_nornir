"""Primeiro contato com o Infrahub via infrahub-sdk (leitura)."""

import os

from infrahub_sdk import Config, InfrahubClientSync

client = InfrahubClientSync(
    address=os.environ.get("INFRAHUB_ADDRESS", "http://10.0.0.3:8000"),
    config=Config(api_token=os.environ.get("INFRAHUB_TOKEN")),
)

devices = client.all(kind="DcimDevice")
print(f"{len(devices)} devices no SoT:")
for device in sorted(devices, key=lambda d: d.name.value):
    print(" -", device.name.value, "| serial:", device.serial.value)
