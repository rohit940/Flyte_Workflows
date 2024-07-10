from datetime import timedelta
from flytekit import Resources,dynamic,task, workflow,dynamic, LaunchPlan, FixedRate
from flytekit.types.file import FlyteFile
import yaml
  
@task(requests=Resources(cpu="1", mem="1000Mi"), limits=Resources(cpu="1", mem="1000Mi"),
    container_image="rohit9988/flytek8sboto3:latest",
    )
def deployment_task_05(config_file : FlyteFile,video_name: str):
    with open(config_file, 'r') as f:
        flytefile_content = f.read()
        config_values = yaml.safe_load(flytefile_content)

    pod_name = video_name.replace(".mp4", "-pod")
    from kubernetes import client, config
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    
    pod = client.V1Pod(
        metadata=client.V1ObjectMeta(name=pod_name),
        spec=client.V1PodSpec(
            containers=[
                client.V1Container(
                    name="source-container",
                    image=config_values["dockerImages"]["source_container_image"],
                    command=[
                        "/bin/bash",
                        "-c",
                        f"sed -i 's/FILENAME/{video_name}/g' source.py && python source.py"
                    ],
                    resources=client.V1ResourceRequirements(
                        requests={"cpu": "300m", "memory": "500Mi"},
                        limits={"cpu": "500m", "memory": "500Mi"},
                    )
                ),
                client.V1Container(
                    name="receiver-container",
                    image=config_values["dockerImages"]["receiver_container_image"],
                    command=[
                        "/bin/bash",
                        "-c",
                        f"sed -i 's/FILENAME/{video_name}/g' receiver.py && python receiver.py"
                    ],
                    resources=client.V1ResourceRequirements(
                        requests={"cpu": "300m", "memory": "500Mi"},
                        limits={"cpu": "500m", "memory": "500Mi"},
                    )
                )
            ]
        )
    )

    v1.create_namespaced_pod(namespace="flytesnacks-development", body=pod)
    return "Pod created."

@dynamic(
    container_image="rohit9988/flytek8sboto3:latest",
    requests=Resources(cpu="300m", mem="1000Mi"),
    limits=Resources(cpu="300m", mem="1000Mi")
)
def monitoring_task_new_05(config_file : FlyteFile):
    import yaml
    import boto3
    with open(config_file, 'r') as f:
        flytefile_content = f.read()
        config_values = yaml.safe_load(flytefile_content)

    bucket_name = config_values['s3_bucket']['bucket_name']
    folder_prefix = config_values["s3_bucket"]["input_folder_prefix"]
    s3_client = boto3.client('s3')
    file_key=config_values["s3_bucket"]["tmp_file_key"]
    try:
        s3_client.download_file(bucket_name, file_key, "prev_tmp.txt")
        with open("prev_tmp.txt", "r") as f:
            old_object_names = [line.strip() for line in f.readlines()]
        objects = []
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name, Prefix=folder_prefix):
            if 'Contents' in page:
                objects.extend([obj['Key'] for obj in page['Contents']])
        current_object_names = objects
        new_object_names = [obj for obj in current_object_names if obj not in old_object_names]
        if new_object_names != []:
            for new_object_name in new_object_names:
                if not new_object_name.endswith('/'):
                    video_name=new_object_name.split('/')[-1]
                    deployment_workflow(config_file=config_file,video_name=video_name)
        else:
            print("No new files found here")
            return "No new files found"
        
        updated_objects=s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
        s3_object_keys = [obj['Key'] for obj in updated_objects.get('Contents', [])]
        file_path = "new_tmp.txt"
        with open(file_path, 'w') as f:
            for key in s3_object_keys:
                if not key.endswith('/'):
                    f.write(key + '\n')
        s3_client.upload_file(file_path, bucket_name, file_key)
        print("File updated and uploaded successfully.")

    except Exception as e:
        return(f"Error: {e}")


@workflow
def monitoring_workflow_new_05(config_file : FlyteFile):
    monitoring_task_new_05(config_file=config_file)
    
@workflow
def deployment_workflow(config_file : FlyteFile, video_name : str):
    deployment_task_05(config_file=config_file,video_name=video_name)

fixed_rate_lp = LaunchPlan.get_or_create(
    name="video_process_lp",
    workflow=monitoring_workflow_new_05,
    schedule=FixedRate(duration=timedelta(minutes=1)),
    # fixed_inputs={"config_file": "workflows/video_process/config.yaml"}
)
