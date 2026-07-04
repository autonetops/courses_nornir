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

## Diretório

- `config.yaml` — configuração do runner (threaded) e inventory plugin (SimpleInventory)
- `inventory/hosts.yaml` — r1–r4 em 172.20.20.11–14
- `inventory/groups.yaml` — grupo `ios_routers` com plataforma `cisco_xe`
- `inventory/defaults.yaml` — valores globais de fallback (sem credenciais)
- `get_version.py` — exemplo: puxa `show version` de todos os roteadores em paralelo

## Próximos Passos

Execute `get_version.py` para confirmar conectividade com os quatro roteadores:

```bash
python get_version.py
```

Você verá a saída de cada roteador formatada por host, rodando em paralelo.
