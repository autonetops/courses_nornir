"""Transform functions do lab: preparam cada host logo apos a carga.

`prepara_host` e registrada no fim do modulo e referenciada pelo
config.yaml (`transform_function: "prepara_host"`). Por isso, TODO
script que faz InitNornir(config_file="config.yaml") precisa de um
`import transform` ANTES do InitNornir — e o import que registra.

`enrich_from_cmdb` e a versao original do Cap. 2, mantida como
historico (external_inventory.py ainda a usa).
"""

import json
import os
from pathlib import Path

from nornir.core.inventory import Host
from nornir.core.plugins.inventory import TransformFunctionRegister

_CMDB_FILE = Path(__file__).parent / "inventory" / "hosts.json"
_CMDB = json.loads(_CMDB_FILE.read_text())
_CAMPOS_CMDB = ("model", "serial", "rack")

# Servicos por site: dado que NAO mora em host nenhum — e derivado.
SERVICOS_POR_SITE = {
    "poa": {"ntp": "10.10.0.1", "dns": "10.10.0.53"},
    "gru": {"ntp": "10.20.0.1", "dns": "10.20.0.53"},
}


def enrich_from_cmdb(host: Host) -> None:
    """Injeta os metadados do CMDB (hosts.json) em cada host (Cap. 2)."""
    extra = _CMDB.get(host.name, {})
    for key, value in extra.items():
        host.data[key] = value


def prepara_host(host: Host) -> None:
    """Credenciais + CMDB + dados derivados, num unico lugar (Cap. 4)."""
    # 1) Credenciais de env — fora dos runbooks. Usamos .get() para que
    #    scripts device-free (render, testes) rodem SEM credenciais;
    #    quem precisa conectar valida as env vars antes (ver deploy.py).
    host.username = host.username or os.environ.get("NORNIR_USER")
    host.password = host.password or os.environ.get("NORNIR_PASS")

    # 2) Enriquecimento do CMDB (hosts.json), como no Cap. 2 — mas so
    #    os campos de interesse, nao o export inteiro.
    extra = _CMDB.get(host.name, {})
    for campo in _CAMPOS_CMDB:
        if campo in extra:
            host.data[campo] = extra[campo]

    # 3) Dados DERIVADOS: calculados a partir do que ja existe.
    #    host.get() resolve a heranca host -> grupos -> defaults.
    if host.hostname:
        ultimo_octeto = host.hostname.rsplit(".", 1)[-1]
        host.data["mgmt_ip"] = f"10.99.0.{ultimo_octeto}"
    servicos = SERVICOS_POR_SITE.get(host.get("site", ""), {})
    for chave, valor in servicos.items():
        host.data.setdefault(chave, valor)


# Registro no import do modulo: os scripts fazem `import transform`
# e o config.yaml conecta a funcao pelo nome.
TransformFunctionRegister.register("prepara_host", prepara_host)
