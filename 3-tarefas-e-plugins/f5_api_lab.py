import os

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result

from tasks.f5_api import f5_versao

nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.username = os.environ["NORNIR_USER"]
nr.inventory.defaults.password = os.environ["NORNIR_PASS"]

# So o F5 — o unico host API-only do inventario.
so_f5 = nr.filter(platform="f5_bigip")
resultado = so_f5.run(task=f5_versao)
print_result(resultado)
