from flytekit import task, workflow
from kubernetes.client.models import (
    V1PodSpec, V1Container, V1ResourceRequirements,
)
from flytekit import task, workflow,PodTemplate

@task(pod_template=PodTemplate(
        primary_container_name="primary",
        labels={"app": "example", "environment": "dev"},
        annotations={"description": "Single container task with Alpine"},
        pod_spec=V1PodSpec(
            containers=[
                V1Container(
                    name="primary",
                    resources=V1ResourceRequirements(
                        requests={"cpu": "100m", "memory": "100Mi"},
                        limits={"cpu": "500m", "memory": "500Mi"},
                    ),
                ),
                V1Container(
                    name="secondary",
                    image="alpine",
                    command=["/bin/sh"],
                    args=[
                        "-c",
                        "echo hi pod world "
                    ],
                    resources=V1ResourceRequirements(
                        requests={"cpu": "100m", "memory": "100Mi"},
                        limits={"cpu": "500m", "memory": "500Mi"},
                    ),
                ),
            ],
        )
    )
)
def hello() :
    return f"Hello!"
@workflow
def wf():
    hello()
    
