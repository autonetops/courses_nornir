from nornir import InitNornir
from nornir_jinja2.plugins.tasks import template_file

nr = InitNornir(config_file="config.yaml")

# Each platform has its own template directory: templates/eos and templates/ios.
# Rendering does NOT connect to anything — it is plain Python running locally.
eos = nr.filter(platform="arista_eos")
r_eos = eos.run(task=template_file, template="base.j2", path="templates/eos")

ios = nr.filter(platform="cisco_ios")
r_ios = ios.run(task=template_file, template="base.j2", path="templates/ios")

print("========== pe-emea-01 (eos) ==========")
print(r_eos["pe-emea-01"].result)
print("========== core-rr-01 (ios) ==========")
print(r_ios["core-rr-01"].result)
