
import typing
from flytekit import task, workflow

@task()
def say_hello(name: str) -> str:
    """A simple Flyte task to say "Hello".

    The @task decorator allows Flyte to use this function as a Flyte task,
    which is executed as an isolated, containerized unit of compute.
    """
    return f"Hello, {name}!"


@task()
def greeting_length(greeting: str) -> int:
    """A task the counts the length of a greeting."""
    return len(greeting)


@workflow
def wf(name: str = "world") -> typing.Tuple[str, int]:
    """Declare workflow called `wf`.

    """
    greeting = say_hello(name=name)
    greeting_len = greeting_length(greeting=greeting)
    return greeting, greeting_len


if __name__ == "__main__":
    # Execute the workflow by invoking it like a function and passing in
    # the necessary parameters
    print(f"Running wf() {wf(name='passengers')}")                                                             
