from fastapi import APIRouter, Depends,HTTPException
import uuid
from services.s3_services import s3_client
from dotenv import load_dotenv
import os

load_dotenv()
AWS_BUCKET =os.getenv('AWS_BUCKET')
#define router
router = APIRouter(
    tags=['/s3_service']
)

@router.get("/get-presigned-url/")
async def get_presigned_url():
    file_key = f"image-zison-{uuid.uuid4().hex[:20]}"
    file_type = 'image/jpeg'  

    try:
        presigned_url = s3_client.generate_presigned_url('put_object',
                                                         Params={'Bucket': AWS_BUCKET, 'Key': file_key, 'ContentType': file_type},
                                                         ExpiresIn=3600)
        return {"url": presigned_url, "key": file_key, "contentType": file_type}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))