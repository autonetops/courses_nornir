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
export NORNIR_USER="admin"
export NORNIR_PASS="autonetops"
```

O script falhará rapidamente (fail-fast) se essas variáveis não estiverem definidas.

## Estrutura de Pastas

Este repositório não vive mais numa única raiz que evolui capítulo a
capítulo — cada capítulo ganha sua própria pasta `N-<tema>`. Cada pasta
`N-<tema>` é o estado completo e autocontido do projeto `nornir-lab/` **ao
fim do capítulo N**: tem seu próprio `config.yaml`, `inventory/`, `tasks/`
etc., prontos para rodar sem depender de nenhuma outra pasta. Como o curso é
cumulativo, pastas mais avançadas repetem (e estendem) os arquivos das
anteriores — a duplicação é intencional. Nas aulas o diretório é sempre
chamado de `nornir-lab/`; entre na pasta do capítulo que você está cursando
e trate-a como se fosse essa raiz:

```bash
cd 4-tecnicas-avancadas   # ou a pasta do capítulo que você está cursando
```

Cada capítulo também é marcado com uma tag `cap-<N>` e um commit
correspondente no histórico do git — são o registro histórico de como o
projeto evoluiu; a pasta é a forma prática de trabalhar com esse estado.

| Capítulo | Pasta | Tag | Descrição |
|----------|-------|-----|-----------|
| 1 | `1-Fundamentals/` | `cap-1` | Fundamentos: config.yaml, inventário, show version |
| 2 | `2-inventario/` | `cap-2` | Gerenciando o Inventário: hierarquia, grupos compostos, filtros, transform |
| 3 | `3-tarefas-e-plugins/` | `cap-3` | Execução de Tarefas e Plugins: tasks custom, netmiko/napalm/scrapli, resultados, dry-run, Jinja2 |
| 4 | `4-tecnicas-avancadas/` | `cap-4` | Técnicas Avançadas: workflow de config reutilizável, transform de credenciais, retry/idempotência, pytest, inventory plugin próprio |
| 5 | `5-arquitetura/` | `cap-5` | A Arquitetura de Automação de Redes: camadas NAF e o mapa do stack (concepts-only) |
| 6 | `6-infrahub/` | `cap-6` | Infrahub como Source of Truth: InfrahubInventory, GraphQL, artifacts, drift |

## Diretório (por capítulo)

- `1-Fundamentals/` — `config.yaml`, `inventory/` (hosts/groups/defaults) e `get_version.py`: primeiro contato, show version nos roteadores
- `2-inventario/` — hierarquia de inventário, grupos compostos, `filter_lab.py` e `transform.py` (`enrich_from_cmdb`), `external_inventory.py`
- `3-tarefas-e-plugins/`:
  - `tasks/facts.py` — task custom sobre netmiko (uptime); `tasks/f5_api.py` — task HTTP iControl REST (F5 API-only)
  - `custom_task_lab.py` — roda a task custom `uptime` (Aula 1)
  - `plugins_lab.py` — netmiko × napalm × scrapli lado a lado (Aula 2)
  - `f5_api_lab.py` — versão do BIG-IP via iControl REST (Aula 2)
  - `processors.py` + `resultado_lab.py` — resultados, `failed_hosts` e processor de progresso (Aula 3, device-free)
  - `config_lab.py` — `napalm_configure` com dry-run, diff e idempotência (Aula 4)
  - `templates/ios/base.j2`, `templates/eos/base.j2` — templates Jinja2 por plataforma (Aula 5)
  - `render_lab.py` — renderiza os templates (device-free); `deploy_from_template.py` — render → deploy (dry-run)
- `4-tecnicas-avancadas/`:
  - `config.yaml` — runner (threaded), SimpleInventory e a transform function `prepara_host`
  - `inventory/hosts.json` — export externo (CMDB simulado) com ip/platform/site/role por host
  - `tasks/config_mgmt.py` — workflow reutilizável render → diff → deploy (`configurar`) + retry limitado (`configurar_com_retry`)
  - `deploy.py` — CLI de deploy com `--site`/`--role`/`--tentativas`/`--commit` e exit codes para CI
  - `erros_lab.py` — taxonomia de falhas, retry e exit code (Aula 3, device-free)
  - `pytest.ini` + `tests/` — suíte pytest com inventário fake (`tests/fixtures/`); roda sem nenhum device (Aula 4)
  - `nornir_lab_inventory.py` — inventory plugin próprio (`LabJSONInventory`) que constrói o inventário do `hosts.json` (Aula 5)
  - `config_plugin.yaml` + `plugin_inventory_lab.py` — inicialização usando o plugin próprio (device-free)
- `5-arquitetura/arquitetura.md` — as camadas NAF e o mapa do stack do curso
- `6-infrahub/`:
  - `sot_lab.py` — primeiro contato com o Infrahub via `infrahub-sdk` (leitura) (Aula 1)
  - `config-infrahub.yaml` — config do Nornir com o `InfrahubInventory` (sem token: injetado de env) (Aula 2)
  - `inventory/group.yaml` — grupos estáticos `platform__ios`/`platform__eos` com `connection_options` napalm/scrapli (Aula 2)
  - `infrahub_inventario.py` — inventário do Nornir nascendo do Infrahub; guarda fail-fast se `nornir_platform` não estiver semeado (Aula 2)
  - `queries/device_config.gql` — query GraphQL parametrizada dos dados de config por device (Aula 3)
  - `templates/ios/interfaces_sot.j2` — template do padrão query → dict → template (Aulas 3–4)
  - `render_sot.py` — executa a query e renderiza a config localmente (Aula 3)
  - `.infrahub.yml` — declaração de queries/transforms/artifact definitions carregada pelo Infrahub no Cap. 7 (Aula 4)
  - `artifacts_lab.py` — gera e puxa o artifact `startup-config` via `nornir-infrahub` (Aula 4)
  - `drift.py` — detecção de drift: intended (artifact do SoT) × running (`napalm get_config`), com exit code para CI (Aula 5)

## Próximos Passos

Em `2-inventario/`, o inventário tem **sete** hosts — e o `f5` é API-only (sem
SSH). Rodar `get_version.py` sem filtro vai falhar no `f5`; isso é proposital e
motiva os filtros do Capítulo 2. Prefira o script filtrado:

```bash
cd 2-inventario
python filter_lab.py
```

Ele aplica `show clock` apenas na fatia `edge & poa` (`r1` e `eos1`), rodando em
paralelo. Para explorar o inventário sem tocar em nenhum dispositivo, rode
`python external_inventory.py`.

Em `3-tarefas-e-plugins/`, os scripts colocam o inventário para **trabalhar**.
Dois deles rodam **sem lab** (Python puro, ótimos para estudar):
`python resultado_lab.py` (resultados, `failed_hosts` e o processor de
progresso) e `python render_lab.py` (renderiza os templates Jinja2 por
plataforma). Os demais (`custom_task_lab.py`, `plugins_lab.py`,
`f5_api_lab.py`, `config_lab.py`, `deploy_from_template.py`) tocam os
dispositivos — exporte as credenciais antes. O deploy é sempre em
`dry_run=True`: revise o diff antes de trocar para `False`.

## Testes (Cap. 4)

Em `4-tecnicas-avancadas/`, a suíte de testes roda **sem nenhum dispositivo**
— inventário fake em `tests/fixtures/`, tasks de rede monkeypatchadas:

```bash
cd 4-tecnicas-avancadas
python -m pytest tests/ -v
```

A partir do Cap. 4, o `config.yaml` referencia a transform function
`prepara_host`; todo script faz `import transform` antes do `InitNornir`
(é o import que registra a função). As credenciais continuam vindo de
`NORNIR_USER`/`NORNIR_PASS` — agora injetadas pela transform, não mais
linha a linha em cada script. Scripts device-free e testes rodam sem as
variáveis; o `deploy.py` valida as env vars antes de conectar (exit 2).
