from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def hello_world(task: Task) -> Result:
    return Result(host=task.host, result=f"Hello, {task.host.hostname}!")


if __name__ == "__main__":
    results = nr.run(task=hello_world)
    print_result(results)
