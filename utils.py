import boto3, uuid

from django.conf import settings

class FileUpload:
    def __init__(self,file):
        self.file = file
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        )

    def upload_file(self):
        url_generator = str(uuid.uuid4())

        self.s3_client.upload_fileobj(
                self.file,
                'prep-test',
                url_generator,
                ExtraArgs={
                    'ContentType' : self.file.content_type
                }
            )
        
        return f"https://prep-test.s3.ap-northeast-2.amazonaws.com/{url_generator}"