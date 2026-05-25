import boto3
import logging
import json
import time

from botocore.exceptions import ClientError


logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)

TASK_DEFINITION = '<task_definition>'
AWS_PROFILE = '<environment>'

if __name__ == '__main__':
    ssm_client = boto3.client('ssm', region_name='us-east-1')
    ecs_client = boto3.client('ecs')

    response = ecs_client.describe_task_definition(taskDefinition=TASK_DEFINITION)

    # env = response['taskDefinition']['containerDefinitions'][0]['environment']

    env_vars = response["taskDefinition"]['containerDefinitions'][0]['environment']
    secrets = response["taskDefinition"]['containerDefinitions'][0]['secrets']
    # log.info(f'RESPONSE ITEMS: {len(env)}')

    env = env_vars + secrets


    config = []

    for var in env:
        if var['name'] == 'TASKIQ_BROKER':
            config.append(f'{var["name"]}=""')
            continue


        name = ''

        if 'value' in list(var.keys()):
            name = var['value']

        else:
            name = var['valueFrom']

            try:
                ssm_value = ssm_client.get_parameter(
                    Name=name,
                    WithDecryption=True
                )['Parameter']['Value']

                config.append(f'{var["name"]}={ssm_value}')
                continue

            except Exception:
                continue

        config.append(f'{var["name"]}={var["value"]}')

    config.append(f'PYTHONUNBUFFERED=1')
    config.append(f'AWS_PROFILE={AWS_PROFILE}')


    log.info(f'\n\n{";".join(config)}')
