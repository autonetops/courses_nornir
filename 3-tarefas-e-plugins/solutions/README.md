# Soluções — Capítulo 3

Cada arquivo aqui é a versão **completa** do exercício de mesmo nome na raiz
do capítulo. Os arquivos da raiz são esqueletos com `TODO`s numerados —
complete-os primeiro e use esta pasta só para conferir (ou destravar).

Para rodar uma solução, entre **nesta** pasta — o `config.yaml` daqui aponta
para o inventário compartilhado em `../inventory/`:

```bash
cd solutions
export NORNIR_USER="admin" NORNIR_PASS="admin"
uv run python resultado_lab.py         # device-free
uv run python render_lab.py            # device-free (Jinja2)
uv run python sonda_lab.py             # nem credenciais precisa
uv run python custom_task_lab.py       # precisa do lab
uv run python plugins_lab.py           # precisa do lab
uv run python config_lab.py            # precisa do lab (dry-run)
uv run python deploy_from_template.py  # precisa do lab (dry-run)
```
