from flytekit import task, workflow, Resources
from flytekit.types.file import FlyteFile

@task(requests=Resources(cpu="1", mem="1000Mi"), limits=Resources(cpu="1", mem="1000Mi"))
def process_file(f_in: FlyteFile) -> int:
    with f_in.open("r") as fh:
        data = fh.read()
    print(data)
    return len(data)

@workflow
def runme(input_file: FlyteFile) -> int:
    return process_file(f_in=input_file)
