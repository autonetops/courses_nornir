"""Testes de template: renderiza e afirma linhas — sem device.

Renderizar e Python puro; se o template quebrar (variavel ausente,
sintaxe errada), quebra AQUI, nao no deploy.
"""

from nornir_jinja2.plugins.tasks import template_file

from tasks.config_mgmt import TEMPLATES_POR_PLATAFORMA


def test_template_ios_renderiza_loopback_e_banner(nr):
    r = nr.filter(name="r1").run(
        task=template_file,
        template="base.j2",
        path=TEMPLATES_POR_PLATAFORMA["cisco_xe"],
    )
    config = r["r1"].result
    assert "ip domain name nornir.lab" in config
    assert "interface Loopback0" in config
    assert " ip address 10.255.0.1 255.255.255.255" in config
    assert "banner login ^C r1 :: poa/edge :: acesso autorizado ^C" in config


def test_template_eos_usa_sintaxe_de_prefixo(nr):
    r = nr.filter(name="eos1").run(
        task=template_file,
        template="base.j2",
        path=TEMPLATES_POR_PLATAFORMA["arista_eos"],
    )
    config = r["eos1"].result
    assert "ip domain-name nornir.lab" in config
    assert "ip address 10.255.0.21/32" in config  # EOS: prefixo, nao mascara
