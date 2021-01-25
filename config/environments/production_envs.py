from ssm_cache import SSMParameterGroup
app_envs = SSMParameterGroup(base_path="/scenario_6/app", max_age=300)

APP_SECRET_KEY = app_envs.parameter('/SECRET_KEY').value

DB_NAME = app_envs.parameter('/DB_NAME').value
DB_USER = app_envs.parameter('/DB_USER').value
DB_PASSWORD = app_envs.parameter('/DB_PASSWORD').value
DB_HOST = app_envs.parameter('/DB_HOST').value
DB_PORT = app_envs.parameter('/DB_PORT').value
