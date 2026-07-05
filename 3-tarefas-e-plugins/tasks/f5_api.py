import os

import requests
import urllib3
from nornir.core.task import Result, Task
from requests.auth import HTTPBasicAuth

# O BIG-IP do lab usa certificado self-signed. Silenciamos o aviso para nao
# poluir a saida. Em PRODUCAO, use verify=<caminho-do-CA> e NUNCA verify=False.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def f5_versao(task: Task) -> Result:
    """Consulta a versao do BIG-IP via iControl REST — automacao SEM CLI.

    O F5 e API-only (`api_only: true` no inventario). Em vez de netmiko,
    falamos com a API HTTPS (iControl REST) usando `requests`. As mesmas
    credenciais (NORNIR_USER/NORNIR_PASS) autenticam via Basic Auth.
    """
    url = f"https://{task.host.hostname}/mgmt/tm/sys/version"
    resposta = requests.get(
        url,
        auth=HTTPBasicAuth(os.environ["NORNIR_USER"], os.environ["NORNIR_PASS"]),
        verify=False,  # lab self-signed — ver nota acima
        timeout=30,
    )
    resposta.raise_for_status()

    # O iControl REST aninha os dados em entries -> nestedStats -> entries.
    dados = resposta.json()
    primeira = next(iter(dados["entries"].values()))
    campos = primeira["nestedStats"]["entries"]
    versao = campos["Version"]["description"]
    produto = campos["Product"]["description"]
    return Result(host=task.host, result={"produto": produto, "versao": versao})
