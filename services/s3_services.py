from uuid import uuid4
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
aws_session_token=os.getenv('AWS_SESSION_TOKEN')
AWS_BUCKET =os.getenv('AWS_BUCKET')
region_name=os.getenv('REGION_NAME')

s3_client = boto3.client('s3',
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key,
                         region_name=region_name)

# s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
#                     aws_session_token=aws_session_token, region_name=region_name)
# bucket = s3.Bucket(AWS_BUCKET)


# async def s3_upload(contents: bytes, key: str):
#     logger.info(f'Uploading {key} to S3')
#     bucket.put_object(Key=key, Body=contents)

# def create_presigned_url(bucket_name: str, object_name: str, expiration=3600):
#     s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
#     try:
#         response = s3_client.generate_presigned_url('get_object',
#                                                     Params={'Bucket': bucket_name, 'Key': object_name},
#                                                     ExpiresIn=expiration)
#     except ClientError as e:
#         logger.error(e)
#         return None
#     return response