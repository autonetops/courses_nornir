import json
from pathlib import Path

from nornir.core.inventory import Host

_CMDB_FILE = Path(__file__).parent / "inventory" / "hosts.json"
_CMDB = json.loads(_CMDB_FILE.read_text())


def enrich_from_cmdb(host: Host) -> None:
    """Injeta os metadados do CMDB (hosts.json) em cada host."""
    extra = _CMDB.get(host.name, {})
    for key, value in extra.items():
        host.data[key] = value
