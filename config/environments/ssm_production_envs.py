from ssm_cache import SSMParameterGroup
app_envs = SSMParameterGroup(base_path="/scenario_6/app", max_age=300)

SECRET_KEY = app_envs.parameter('/SECRET_KEY').value

AWS_STORAGE_BUCKET_NAME = app_envs.parameter('/AWS_STORAGE_BUCKET_NAME').value
CLOUDFRONT_URL = app_envs.parameter('/CLOUDFRONT_URL').value
CLOUDFRONT_PRIVATE_KEY = app_envs.parameter('/CLOUDFRONT_PRIVATE_KEY').value
CLOUDFRONT_KEY_PAIR_ID = app_envs.parameter('/CLOUDFRONT_KEY_PAIR_ID').value

DB_NAME = app_envs.parameter('/DB_NAME').value
DB_USER = app_envs.parameter('/DB_USER').value
DB_PASSWORD = app_envs.parameter('/DB_PASSWORD').value
DB_HOST = app_envs.parameter('/DB_HOST').value
DB_PORT = app_envs.parameter('/DB_PORT').value

