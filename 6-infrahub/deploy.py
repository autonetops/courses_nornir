"""CLI de deploy: render -> diff -> aprovacao (flag) -> commit.

Uso:
    python deploy.py                  # dry-run em todos (padrao seguro)
    python deploy.py --site poa       # limita a um site
    python deploy.py --role edge      # limita a um papel
    python deploy.py --tentativas 3   # retry para falhas transitorias
    python deploy.py --commit         # aplica DE VERDADE

Exit codes (prontos para CI, Cap. 7):
    0 = sucesso (com ou sem mudancas)
    1 = ao menos um host falhou
    2 = erro de uso (sem credenciais / selecao vazia)
"""

import argparse
import os
import sys

from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result

import transform  # noqa: F401  (registra "prepara_host" do config.yaml)
from tasks.config_mgmt import TEMPLATES_POR_PLATAFORMA, configurar_com_retry


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Deploy de configuracao via Nornir")
    p.add_argument("--site", help="limita a um site (ex.: poa, gru)")
    p.add_argument("--role", help="limita a um papel (ex.: edge, core)")
    p.add_argument(
        "--commit",
        action="store_true",
        help="comita de verdade (sem esta flag e dry-run)",
    )
    p.add_argument(
        "--tentativas",
        type=int,
        default=1,
        help="tentativas por host para falhas transitorias (padrao: 1)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    # Fail-fast no CLI: quem conecta precisa de credenciais.
    for var in ("NORNIR_USER", "NORNIR_PASS"):
        if var not in os.environ:
            print(f"erro: variavel de ambiente {var} nao definida", file=sys.stderr)
            return 2

    nr = InitNornir(config_file="config.yaml")

    # So plataformas com template (o f5 fica de fora — API-only).
    alvo = nr.filter(F(platform__any=sorted(TEMPLATES_POR_PLATAFORMA)))
    if args.site:
        alvo = alvo.filter(site=args.site)
    if args.role:
        alvo = alvo.filter(role=args.role)
    if not alvo.inventory.hosts:
        print("erro: nenhum host selecionado", file=sys.stderr)
        return 2

    modo = "COMMIT" if args.commit else "dry-run"
    nomes = ", ".join(sorted(alvo.inventory.hosts))
    print(f"== deploy ({modo}) em {len(alvo.inventory.hosts)} host(s): {nomes}")

    resultado = alvo.run(
        task=configurar_com_retry,
        commit=args.commit,
        tentativas=args.tentativas,
    )
    print_result(resultado)

    # Falha parcial NUNCA passa despercebida: relatorio + exit code != 0.
    if resultado.failed:
        falhos = ", ".join(sorted(resultado.failed_hosts))
        print(
            f"\nFALHA em {len(resultado.failed_hosts)} host(s): {falhos}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
