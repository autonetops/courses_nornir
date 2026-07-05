"""Padrao query -> dict -> template: renderiza config a partir do SoT.

Parte 1 puxa os dados do Infrahub por GraphQL; parte 2 achata o dict num
contexto e renderiza com Jinja2 (templates/ios/interfaces_sot.j2).
"""

import os
from pathlib import Path

import jinja2
from infrahub_sdk import Config, InfrahubClientSync

# --- parte 1: puxar os dados ---
client = InfrahubClientSync(
    address=os.environ.get("INFRAHUB_ADDRESS", "http://10.0.0.3:8000"),
    config=Config(api_token=os.environ.get("INFRAHUB_TOKEN")),
)

query = Path("queries/device_config.gql").read_text(encoding="utf-8")
data = client.execute_graphql(query, variables={"device": "r1"})

device = data["DcimDevice"]["edges"][0]["node"]
print("device:", device["name"]["value"])
print("platform:", device["platform"]["node"]["nornir_platform"]["value"])
for edge in device["interfaces"]["edges"]:
    iface = edge["node"]
    print(" -", iface["name"]["value"], "|", iface["description"]["value"])


# --- parte 2: dict -> template ---
def contexto_do_device(data: dict) -> dict:
    node = data["DcimDevice"]["edges"][0]["node"]
    return {
        "hostname": node["name"]["value"],
        "interfaces": [
            {
                "nome": e["node"]["name"]["value"],
                "descricao": e["node"]["description"]["value"],
            }
            for e in node["interfaces"]["edges"]
        ],
    }


TEMPLATE = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates/ios"),
    trim_blocks=True,
    lstrip_blocks=True,
)

contexto = contexto_do_device(data)
config = TEMPLATE.get_template("interfaces_sot.j2").render(**contexto)
print(config)
