from nornir import InitNornir
from nornir_jinja2.plugins.tasks import template_file

nr = InitNornir(config_file="config.yaml")

# Cada plataforma tem seu diretorio de templates: templates/ios e templates/eos.
# Renderizar NAO conecta em nada — e Python puro rodando local.
ios = nr.filter(platform="cisco_xe")
r_ios = ios.run(task=template_file, template="base.j2", path="templates/ios")

eos = nr.filter(platform="arista_eos")
r_eos = eos.run(task=template_file, template="base.j2", path="templates/eos")

print("========== r1 (ios) ==========")
print(r_ios["r1"].result)
print("========== eos1 (eos) ==========")
print(r_eos["eos1"].result)
