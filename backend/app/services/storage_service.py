import boto3
from botocore.exceptions import ClientError
from typing import Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.AWS_S3_BUCKET
    
    def upload_file(self, file_path: str, object_name: str) -> bool:
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            return True
        except ClientError as e:
            logger.error(f"Error uploading file to S3: {e}")
            return False
    
    def download_file(self, object_name: str, file_path: str) -> bool:
        try:
            self.s3_client.download_file(self.bucket_name, object_name, file_path)
            return True
        except ClientError as e:
            logger.error(f"Error downloading file from S3: {e}")
            return False
    
    def delete_file(self, object_name: str) -> bool:
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
            return True
        except ClientError as e:
            logger.error(f"Error deleting file from S3: {e}")
            return False
    
    def generate_presigned_url(
        self,
        object_name: str,
        expiration: int = 3600
    ) -> Optional[str]:
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None
    
    def generate_presigned_post(
        self,
        object_name: str,
        expiration: int = 3600
    ) -> Optional[dict]:
        try:
            response = self.s3_client.generate_presigned_post(
                self.bucket_name,
                object_name,
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            logger.error(f"Error generating presigned POST: {e}")
            return None

