from nornir import InitNornir
from nornir.plugins.functions.text import print_result

nr = InitNornir(config_file="config.yaml")

def hello_world(task):
    task.run(task="debug", msg=f"Hello, {task.host.name}!")


if __name__ == "__main__":
    resultado = nr.run(task=hello_world)
    print_result(resultado)