import time
from datetime import timedelta
from pathlib import Path
from typing import List
from flytekit import Resources, TaskMetadata,dynamic, map_task, task, workflow, ImageSpec,dynamic, LaunchPlan, FixedRate

from flytekitplugins.pod import Pod
from kubernetes.client.models import (
    V1Container,
    V1PodSpec,
    V1ResourceRequirements,
    V1VolumeMount
)
import time
from pathlib import Path
from typing import List

from flytekit import ImageSpec, Resources, TaskMetadata, dynamic, map_task, task, workflow
from flytekitplugins.pod import Pod
from kubernetes.client.models import (
    V1Container,
    V1EmptyDirVolumeSource,
    V1PodSpec,
    V1ResourceRequirements,
    V1Volume,
    V1VolumeMount,
)

image_spec = ImageSpec(registry="ghcr.io/flyteorg", packages=["flytekitplugins-pod"])
_SHARED_DATA_PATH="/data/message.txt"
#video_name="Hello"
image_definition = ImageSpec(
    name="flytekit",
    base_image="ghcr.io/flyteorg/flytekit:py3.11-1.10.2",
    packages=["pandas", "boto3"],
    registry="rohit9988",
    python_version="3.11"
)
@dynamic(
    container_image=image_definition,
    requests=Resources(cpu="200m", mem="1000Mi"),
    limits=Resources(cpu="200m", mem="1000Mi"))
def fetch_s3() -> List[str]:

    import boto3
    s3 = boto3.client('s3')
    bucket_name="mercedesvideosdata"
    file_key="rohit_tmp_object.txt"
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_content = response['Body'].read().decode('utf-8')


    file_names = []
    for line in file_content.splitlines():
        if line.strip():
            if not line.startswith("processed_"): 
                file_name = line.split('/')[-1].split(' - ')[0].strip()
                file_names.append(file_name.split()[-1])
    processed_results = []
    if file_names:
        for file_name in file_names:
            result = deployment_task(video_name=file_name)
            processed_results.append(result)
    else:
        no_new_file()

    return processed_results

@task(requests=Resources(cpu="200m", mem="500Mi"),
    limits=Resources(cpu="200m", mem="500Mi"))
def no_new_file():
    return "No new files"
    
@task(
    requests=Resources(cpu="200m", mem="100Mi"),
    limits=Resources(cpu="200m", mem="100Mi"))
def process(file_name:str) -> str:
    return file_name
@task(
    task_config=Pod(
        pod_spec=V1PodSpec(
            containers=[
                V1Container(
                    name="primary",
                    command=["sleep 300"],
                    resources=V1ResourceRequirements(
                        requests={"cpu": "500m", "memory": "100Mi"},
                        limits={"cpu": "500m", "memory": "100Mi"},
                    ),
                    volume_mounts=[
                        V1VolumeMount(
                            name="shared-data",
                            mount_path="/data",
                        )
                    ],
                ),
                V1Container(
                    name="source",
                    image="mohammed2asif/source:3",
                    command = [
    "/bin/bash", "-c",
    "sleep 5; export MESSAGE_CONTENT=$(cat /data/message123.txt) && echo Filename is $MESSAGE_CONTENT && sed -i 's/{FILENAME}/'\"$MESSAGE_CONTENT\"'/g' app_source.py && python app_source.py"
],
    
                    resources=V1ResourceRequirements(
                        requests={"cpu": "200m", "memory": "100Mi"},
                        limits={"cpu": "200m", "memory": "100Mi"},
                    ),

                    volume_mounts=[
                        V1VolumeMount(
                            name="shared-data",
                            mount_path="/data",
                            read_only=False,
                        )
                    ],
                ),

                V1Container(
                    name="receiver",
                    image="mohammed2asif/receriver-1:2",
                    command = [
    "/bin/bash", "-c",
    "sleep 5; export MESSAGE_CONTENT=$(cat /data/message123.txt);echo Filename is $MESSAGE_CONTENT && sed -i 's/FILENAME/'\"$MESSAGE_CONTENT\"'/g' receiver.py && python receiver.py && sleep 300"
],

                    resources=V1ResourceRequirements(
                        requests={"cpu": "200m", "memory": "100Mi"},
                        limits={"cpu": "200m", "memory": "100Mi"},
                    ),
                    volume_mounts=[
                        V1VolumeMount(
                            name="shared-data",
                            mount_path="/data",
                            read_only=False,
                        )
                    ],
                ),
            ],
            volumes=[
                V1Volume(
                    name="shared-data",
                    empty_dir=V1EmptyDirVolumeSource(medium="Memory"),
                )
            ],
        ),
    ),
    requests=Resources(
        mem="1G",
    ),
)
def deployment_task(video_name:str) -> str:
    directory_path = "/data/"
    import os
    os.makedirs(directory_path, exist_ok=True)
    file_path = "/data/message123.txt"
    with open(file_path, 'w') as file:
        file.write(video_name + '\n')
    return (video_name)


@workflow
def deployment_workflow():
    fetch_s3()


fixed_rate_lp = LaunchPlan.get_or_create(
    name="my_fixed_rate_lp",
    workflow=deployment_workflow,
    schedule=FixedRate(duration=timedelta(minutes=1)),
    #fixed_inputs={"name": "you"},
)
