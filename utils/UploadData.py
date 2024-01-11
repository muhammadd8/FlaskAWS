import boto3

class UploadData:
    def __init__(self) -> None:
        self.aws_access_key = "AKIA5FTZCAUESUQRSNZY"
        self.aws_secret_key = "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"
        self.region_name = "eu-north-1"
        self.s3_key = ""


    def upload(self, file_name, bucket):
        object_name = file_name
        s3_client = boto3.client('s3', aws_access_key_id=self.aws_access_key, aws_secret_access_key=self.aws_secret_key, region_name=self.region_name)
        self.s3_key = f"dataset/{object_name}"
        try:
            response = s3_client.upload_file(file_name, bucket, self.s3_key)
            return True, response
        except Exception as e:
            return False, str(e)