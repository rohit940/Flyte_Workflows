"""A basic Flyte project template that uses ImageSpec"""

import typing
import time
from flytekit import task, workflow, Resources, LaunchPlan



@task(requests=Resources(cpu="1", mem="1000Mi"), limits=Resources(cpu="2", mem="1000Mi"))
def say_hello(name: str):
   # import boto3
    """A simple Flyte task to say "Hello".

    The @task decorator allows Flyte to use this function as a Flyte task,
    which is executed as an isolated, containerized unit of compute.
    """
    time.sleep(300)
    # return f"Hello, {name}!"


@task(requests=Resources(cpu="1", mem="1000Mi"), limits=Resources(cpu="2", mem="1000Mi"))
def greeting_length(greeting: str) -> int:
    """A task the counts the length of a greeting."""
    return len(greeting)


@workflow
def parallel_wf_2(name: str = "world") :
    """Declare workflow called `wf`.

    The @workflow decorator defines an execution graph that is composed of
    tasks and potentially sub-workflows. In this simple example, the workflow
    is composed of just one task.

    There are a few important things to note about workflows:
    - Workflows are a domain-specific language (DSL) for creating execution
      graphs and therefore only support a subset of Python's behavior.
    - Tasks must be invoked with keyword arguments
    - The output variables of tasks are Promises, which are placeholders for
      values that are yet to be materialized, not the actual values.
    """
    greeting = say_hello(name=name)
    greeting = say_hello(name=name)
    greeting = say_hello(name=name)
    # greeting_len = greeting_length(greeting=greeting)
    # return greeting, greeting_len


if __name__ == "__main__":
    # Execute the workflow by invoking it like a function and passing in
    # the necessary parameters
    print(f"Running wf() {parallel_wf_2(name='passengers')}")

launch_plan = LaunchPlan.get_or_create(
    workflow=parallel_wf_2,
    name="max_task_parallelism_lp",
    max_parallelism=2,
)