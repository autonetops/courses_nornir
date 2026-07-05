# Nornir: da Execução à Arquitetura

Este repositório contém os arquivos de laboratório para o curso **Nornir: da Execução à Arquitetura** — uma jornada desde os fundamentos de automação de rede em Python até uma arquitetura de produção (Network Automation Framework / NAF) com Infrahub, GitLab CI e Prefect.

## Clone

```bash
git clone <url> nornir-lab
cd nornir-lab
```

## Credenciais

As credenciais nunca são hardcoded. Antes de rodar qualquer script, exporte as variáveis de ambiente:

```bash
export NORNIR_USER="student"
export NORNIR_PASS="autonetops123"
```

O script falhará rapidamente (fail-fast) se essas variáveis não estiverem definidas.

## Estrutura de Capítulos

Cada capítulo é marcado com uma tag `cap-<N>` e um commit correspondente.

| Capítulo | Tag | Descrição | Status |
|----------|-----|-----------|--------|
| 1 | `cap-1` | Fundamentos: config.yaml, inventário, show version | ✓ Pronto |
| 2 | `cap-2` | Gerenciando o Inventário: hierarquia, grupos compostos, filtros, transform | ✓ Pronto |
| 3 | `cap-3` | Execução de Tarefas e Plugins: tasks custom, netmiko/napalm/scrapli, resultados, dry-run, Jinja2 | ✓ Pronto |
| 4 | `cap-4` | Técnicas Avançadas: workflow de config reutilizável, transform de credenciais, retry/idempotência, pytest, inventory plugin próprio | ✓ Pronto |

## Diretório

- `config.yaml` — runner (threaded), SimpleInventory e a transform function `prepara_host` (Cap. 4)
- `inventory/hosts.yaml` — r1–r4, eos1–eos2 e f5 (172.20.20.11–14/21–22/31) com grupos compostos + `loopback_ip` por host (Cap. 3)
- `inventory/groups.yaml` — grupos por dimensão; `connection_options` de netmiko/napalm/scrapli nos grupos `ios`/`eos` (Cap. 3)
- `inventory/defaults.yaml` — valores globais de fallback (sem credenciais)
- `inventory/hosts.json` — export externo (CMDB simulado); a partir do Cap. 4 traz também ip/platform/site/role por host
- `get_version.py` — exemplo: puxa `show version` de todos os roteadores em paralelo
- `filter_lab.py` — filtra o inventário (edge de POA) e roda `show clock` só na fatia
- `transform.py` — transform functions: `prepara_host` (credenciais + CMDB + dados derivados, Cap. 4) e `enrich_from_cmdb` (Cap. 2)
- `external_inventory.py` — carrega o inventário aplicando a transform function do CMDB
- `tasks/facts.py` — task custom sobre netmiko (uptime); `tasks/f5_api.py` — task HTTP iControl REST (F5 API-only)
- `custom_task_lab.py` — roda a task custom `uptime` (Cap. 3, Aula 1)
- `plugins_lab.py` — netmiko × napalm × scrapli lado a lado (Cap. 3, Aula 2)
- `f5_api_lab.py` — versão do BIG-IP via iControl REST (Cap. 3, Aula 2)
- `processors.py` + `resultado_lab.py` — resultados, `failed_hosts` e processor de progresso (Cap. 3, Aula 3)
- `config_lab.py` — `napalm_configure` com dry-run, diff e idempotência (Cap. 3, Aula 4)
- `templates/ios/base.j2`, `templates/eos/base.j2` — templates Jinja2 por plataforma (Cap. 3, Aula 5)
- `render_lab.py` — renderiza os templates (device-free); `deploy_from_template.py` — render → deploy (dry-run)
- `tasks/config_mgmt.py` — workflow reutilizável render → diff → deploy (`configurar`) + retry limitado (`configurar_com_retry`) (Cap. 4)
- `deploy.py` — CLI de deploy com `--site`/`--role`/`--tentativas`/`--commit` e exit codes para CI (Cap. 4)
- `erros_lab.py` — taxonomia de falhas, retry e exit code, device-free (Cap. 4, Aula 3)
- `pytest.ini` + `tests/` — suíte pytest com inventário fake (`tests/fixtures/`); roda sem nenhum device (Cap. 4, Aula 4)
- `nornir_lab_inventory.py` — inventory plugin próprio (`LabJSONInventory`) que constrói o inventário do `hosts.json` (Cap. 4, Aula 5)
- `config_plugin.yaml` + `plugin_inventory_lab.py` — inicialização usando o plugin próprio (device-free)

## Próximos Passos

A partir do `cap-2` o inventário tem **sete** hosts — e o `f5` é API-only (sem
SSH). Rodar `get_version.py` sem filtro vai falhar no `f5`; isso é proposital e
motiva os filtros do Capítulo 2. Prefira o script filtrado:

```bash
python filter_lab.py
```

Ele aplica `show clock` apenas na fatia `edge & poa` (`r1` e `eos1`), rodando em
paralelo. Para explorar o inventário sem tocar em nenhum dispositivo, rode
`python external_inventory.py`.

No `cap-3` os scripts colocam o inventário para **trabalhar**. Dois deles rodam
**sem lab** (Python puro, ótimos para estudar): `python resultado_lab.py`
(resultados, `failed_hosts` e o processor de progresso) e `python render_lab.py`
(renderiza os templates Jinja2 por plataforma). Os demais (`custom_task_lab.py`,
`plugins_lab.py`, `f5_api_lab.py`, `config_lab.py`, `deploy_from_template.py`)
tocam os dispositivos — exporte as credenciais antes. O deploy é sempre em
`dry_run=True`: revise o diff antes de trocar para `False`.

## Testes (Cap. 4)

A suíte de testes roda **sem nenhum dispositivo** — inventário fake em
`tests/fixtures/`, tasks de rede monkeypatchadas:

```bash
python -m pytest tests/ -v
```

A partir do Cap. 4, o `config.yaml` referencia a transform function
`prepara_host`; todo script faz `import transform` antes do `InitNornir`
(é o import que registra a função). As credenciais continuam vindo de
`NORNIR_USER`/`NORNIR_PASS` — agora injetadas pela transform, não mais
linha a linha em cada script. Scripts device-free e testes rodam sem as
variáveis; o `deploy.py` valida as env vars antes de conectar (exit 2).
