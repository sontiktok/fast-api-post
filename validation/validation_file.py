from uuid import uuid4
import magic
from fastapi import  HTTPException, UploadFile, status


KB = 1024
MB = 1024 * KB
SUPPORTED_FILE_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'application/pdf': 'pdf'
}
async def validate_file(file: UploadFile):
    contents = await file.read()
    size = len(contents)
    if not 0 < size <= 1 * MB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Supported file size is 0 - 1 MB')
    file_type = magic.from_buffer(buffer=contents, mime=True)
    if file_type not in SUPPORTED_FILE_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Unsupported file type: {file_type}. Supported types are {SUPPORTED_FILE_TYPES}')
    return contents, file_type