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

## Diretório

- `config.yaml` — configuração do runner (threaded) e inventory plugin (SimpleInventory)
- `inventory/hosts.yaml` — r1–r4, eos1–eos2 e f5 (172.20.20.11–14/21–22/31) com grupos compostos
- `inventory/groups.yaml` — grupos por dimensão: plataforma (`ios`/`eos`/`f5`), site (`site_poa`/`site_gru`) e papel (`edge`/`core`/`lb`)
- `inventory/defaults.yaml` — valores globais de fallback (sem credenciais)
- `inventory/hosts.json` — export externo (CMDB simulado) com model/serial/rack por host
- `get_version.py` — exemplo: puxa `show version` de todos os roteadores em paralelo
- `filter_lab.py` — filtra o inventário (edge de POA) e roda `show clock` só na fatia
- `transform.py` — transform function que enriquece cada host a partir do `hosts.json`
- `external_inventory.py` — carrega o inventário aplicando a transform function do CMDB

## Próximos Passos

Execute `get_version.py` para confirmar conectividade com os quatro roteadores:

```bash
python get_version.py
```

Você verá a saída de cada roteador formatada por host, rodando em paralelo.
