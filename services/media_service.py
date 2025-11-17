"""
Media service for handling file uploads and storage.
Ready for integration with S3, CloudFlare, or other storage providers.
"""
import os
from werkzeug.utils import secure_filename


class MediaService:
    """
    Media storage service.
    Can be extended to support S3, CloudFlare R2, Azure Blob Storage, etc.
    """
    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in MediaService.ALLOWED_EXTENSIONS
    
    @staticmethod
    def upload_local(file, upload_folder):
        """
        Upload file to local storage.
        For production, replace with S3 or other cloud storage.
        """
        if not file or not MediaService.allowed_file(file.filename):
            return None, 'Invalid file type'
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        
        try:
            os.makedirs(upload_folder, exist_ok=True)
            file.save(filepath)
            return filename, None
        except Exception as e:
            return None, f'Upload failed: {str(e)}'
    
    @staticmethod
    def upload_s3(file, bucket_name, key):
        """
        Placeholder for S3 upload.
        Implement with boto3 for production use.
        
        Example:
            import boto3
            s3_client = boto3.client('s3')
            s3_client.upload_fileobj(file, bucket_name, key)
            return f'https://{bucket_name}.s3.amazonaws.com/{key}'
        """
        raise NotImplementedError('S3 upload not yet implemented')
    
    @staticmethod
    def upload_cloudflare(file, account_id, image_delivery_url):
        """
        Placeholder for CloudFlare Images upload.
        Implement with CloudFlare API for production use.
        """
        raise NotImplementedError('CloudFlare upload not yet implemented')
    
    @staticmethod
    def delete_local(filename, upload_folder):
        """Delete file from local storage."""
        filepath = os.path.join(upload_folder, filename)
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
            return True, None
        except Exception as e:
            return False, f'Delete failed: {str(e)}'
    
    @staticmethod
    def delete_s3(bucket_name, key):
        """
        Placeholder for S3 deletion.
        Implement with boto3 for production use.
        """
        raise NotImplementedError('S3 deletion not yet implemented')
    
    @staticmethod
    def get_storage_url(storage_key, provider='local', base_url='/uploads'):
        """
        Get URL for accessing stored media.
        Adapts based on storage provider.
        """
        if provider == 'local':
            return f'{base_url}/{storage_key}'
        elif provider == 's3':
            # Return S3 URL
            return f'https://your-bucket.s3.amazonaws.com/{storage_key}'
        elif provider == 'cloudflare':
            # Return CloudFlare Images URL
            return f'https://imagedelivery.net/your-account/{storage_key}/public'
        else:
            return storage_key
