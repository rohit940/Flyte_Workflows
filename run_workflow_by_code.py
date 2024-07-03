from flytekit.remote import FlyteRemote
from flytekit.configuration import Config
from flytekit import LaunchPlan


config = Config.auto(config_file="../flyte_config.yaml")

remote = FlyteRemote(
    # config=Config.for_endpoint(endpoint="dns:///localhost:8089"),
    config=config,
    default_project="flytesnacks",
    default_domain="development",
    insecure="true"
)

flyte_lp = remote.fetch_launch_plan(
    name="example.wf", version="3pdLTAyGVs60m185X-HSkA", project="flytesnacks", domain="development"
)

execution = remote.execute(
    flyte_lp, inputs={"name": "test"}, execution_name="test-1234", wait=True
)

print(execution)
