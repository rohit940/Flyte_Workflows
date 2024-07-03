**Register the workflow :**
pyflyte --config config.yaml register --project flytesnacks --domain development workflow.py --version v1
**Activate the Launch Plan**
flytectl update launchplan -p flytesnacks -d development my_fixed_rate_lp --version v1 --activate
