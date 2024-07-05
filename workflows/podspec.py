from flytekit import task, workflow, Resources, ImageSpec
from flytekit.types.file import FlyteFile

from flytekit import task, workflow

import os
from flytekit import ImageSpec, Resources, TaskMetadata, dynamic, map_task, task, workflow
from flytekitplugins.pod import Pod

@task(requests=Resources(cpu="1", mem="1000Mi"), limits=Resources(cpu="1", mem="1000Mi"),
    container_image="rohit9988/k8sflyte:1"
    )
def create_pod(image: str, name: str) -> str:
    from kubernetes import client, config
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    
    pod = client.V1Pod(
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1PodSpec(
            containers=[client.V1Container(
                name=name,
                image=image,
                resources=client.V1ResourceRequirements(
                    requests={"cpu": "100m", "memory": "200Mi"},
                    limits={"cpu": "500m", "memory": "500Mi"},
                )
            )]
        )
    )
    
    v1.create_namespaced_pod(namespace="flytesnacks-development", body=pod)
    return f"Pod {name} with image {image} created."

 

@workflow
def create_pod_wf() -> str:
    return create_pod(image="nginx", name="test")
