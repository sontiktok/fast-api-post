from uuid import uuid4
import boto3
from botocore.exceptions import ClientError
from loguru import logger
from dotenv import load_dotenv
import os

load_dotenv()

aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
aws_session_token=os.getenv('AWS_SESSION_TOKEN')
AWS_BUCKET =os.getenv('AWS_BUCKET')
region_name=os.getenv('REGION_NAME')


s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
def server_create_presigned_url(bucket_name: str, image_key: str, expiration=3600):
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': AWS_BUCKET, 'Key': image_key},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logger.error(e)
        return None
    return response