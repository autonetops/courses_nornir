# nornir-lab

Repositorio de automacao de rede com Nornir — o inventario nasce do Infrahub
(Source of Truth), a config e renderizada de artifacts e o deploy roda atras de
um pipeline GitOps no GitLab CI.

## Onboarding (comece por aqui)

```bash
git clone <url-do-projeto> nornir-lab
cd nornir-lab

# ambiente
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# credenciais e token (NUNCA hardcoded — sempre por env var)
export NORNIR_USER="student"
export NORNIR_PASS="autonetops123"
export INFRAHUB_TOKEN="<seu-token-do-infrahub>"
```

## O que roda sem lab

- `python -m pytest tests/ -q` — a suite de testes (inventario fake, sem device).
- `ruff check .` e `ruff format --check .` — lint e formatacao (instale com
  `pip install ruff`; nao e dependencia de runtime).

## O que toca a rede

- `python deploy.py` — dry-run: renderiza, calcula o diff e faz rollback.
  **Revise o diff.**
- `python deploy.py --commit` — aplica de verdade (idempotente: diff vazio =
  no-op). Exit codes: `0` ok, `1` falha em host, `2` erro de uso.
- `python drift.py` — compara o intended (SoT) com o running (device).

## Pipeline (`.gitlab-ci.yml`)

`lint` -> `test` -> `dry-run` -> `deploy`. Os tres primeiros rodam em todo push
e Merge Request; o `dry-run` publica o diff como artefato. O `deploy` e
**manual** e so na `main` — ninguem muda a rede sem revisar o diff e clicar.

## Regra de ouro: proteja a `main`

Nada entra na `main` por push direto. Toda mudanca vira um **Merge Request**,
passa pelo pipeline (lint + test + dry-run verdes) e por revisao humana antes
do merge. Configure em **Settings > Repository > Protected branches**.

## Estrutura

```
nornir-lab/
├── .gitlab-ci.yml          # pipeline GitOps (lint/test/dry-run/deploy)
├── requirements.txt        # stack fixado do curso
├── ruff.toml               # config do lint
├── .infrahub.yml           # queries/transforms/artifacts do SoT
├── config.yaml             # Nornir + SimpleInventory + transform
├── config-infrahub.yaml    # Nornir + InfrahubInventory (SoT)
├── deploy.py               # CLI de deploy (dry-run/commit, exit codes)
├── drift.py                # deteccao de drift intended x running
├── tasks/                  # workflow reutilizavel (config_mgmt, f5_api, facts)
├── templates/              # Jinja2 por plataforma (ios/eos)
├── queries/                # GraphQL (.gql) do Infrahub
├── inventory/              # hosts/groups/defaults + hosts.json (CMDB)
└── tests/                  # pytest (device-free)
```
