from flytekit import task, workflow, ImageSpec, Resources, FlyteContextManager
import boto3
from datetime import datetime
import time


bucket_name = 'mercedesvideosdata'
folder_prefix = 'data/input/'
image_definition = ImageSpec(
    name="flytekit",
    base_image="ghcr.io/flyteorg/flytekit:py3.11-1.10.2",
    packages=["pandas", "boto3"],
    registry="rohit9988",
    python_version="3.11"
)

@task(
    container_image=image_definition,
    requests=Resources(cpu="200m", mem="1000Mi"),
    limits=Resources(cpu="200m", mem="1000Mi")
)
def monitoring_task():
    s3_client = boto3.client('s3')
    file_key="rohit_tmp_object.txt"
    processed_filenames = set()
    while True:
        try:
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
            file_path = "test.txt"
            with open(file_path, 'w') as f:
                if 'Contents' in response:
                    for obj in response['Contents']:
                        if not obj['Key'].endswith('/'):
                            if obj['Key'] not in processed_filenames:
                                last_modified = obj['LastModified'].astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
                                print("IF")
                                f.write(f"{obj['Key']} - {last_modified}\n")
                                processed_filenames.add(obj['Key'])
                            else:
                                print("ELSE")
                                last_modified = obj['LastModified'].astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
                                processed_key = f"processed_{obj['Key']}"
                                f.write(f"{processed_key} - {last_modified}\n")
                                processed_filenames.add(obj['Key'])
            s3_client.upload_file(file_path, bucket_name, file_key)
        
            print("File updated and uploaded successfully.")
            time.sleep(60)

        except Exception as e:
            print(f"Error: {e}")

@workflow
def monitoring_workflow():
    monitoring_task()
if __name__ == "__main__":
    create_test_file_workflow()
