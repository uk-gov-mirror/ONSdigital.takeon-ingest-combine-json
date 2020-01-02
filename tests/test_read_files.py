import os
import tempfile
import unittest
import boto3
import botocore
from moto import mock_s3
from read_ingestion_bucket import read_file, list_files
MOCK_BUCKET = "mock_bucket"
MY_PREFIX = "mock_folder"

@mock_s3
class TestReadFiles(unittest.TestCase):
    def setUp(self):
        client = boto3.client(
            "s3",
            region_name="eu-west-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
            )
        try:
            s3 = boto3.resource(
                "s3",
                region_name="eu-west-1",
                aws_access_key_id="fake_access_key",
                aws_secret_access_key="fake_secret_key",
                )
            s3.meta.client.head_bucket(Bucket=MOCK_BUCKET)
        except botocore.exceptions.ClientError:
            pass
        else:
            err = "{bucket} should not exist.".format(bucket=MOCK_BUCKET)
            raise EnvironmentError(err)
        client.create_bucket(Bucket=MOCK_BUCKET)
        current_dir = os.path.dirname(__file__)
        fixtures_dir = os.path.join(current_dir, "fixtures")
        upload_mockfiles(MOCK_BUCKET, fixtures_dir)
  
    def tearDown(self):
        s3 = boto3.resource(
            "s3",
            region_name="eu-west-2",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
            )
        bucket = s3.Bucket(MOCK_BUCKET)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

    def upload_mockfiles(self, bucket: str, mock_folder: str) -> None:
        client = boto3.client("s3")
        mockfolder_path = [
            os.path.join(path, filename)
            for path, _, files in os.walk(mock_folder)
            for filename in files
        ]
        for path in mockfolder_path:
            key = os.path.relpath(path, mock_folder)
            client.upload_file(Filename=path, Bucket=bucket, Key=key)

    def test_download_json_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            list_files(MOCK_BUCKET, MY_PREFIX, tmpdir)
            mock_folder_local_path = os.path.join(tmpdir, MY_PREFIX)
            self.assertTrue(os.path.isdir(mock_folder_local_path))
            result = os.listdir(mock_folder_local_path)
            desired_result = ["mock_json.json", "49990000000-200901-0066-02:01:2020-09:56:14-1d253218-2d46-11ea-9b6f-62f53d2f80d6.json", "49990000000-200901-0066-02:01:2020-09:57:32-4b96cf94-2d46-11ea-bf5d-8aa9c757b01f.json"]
            self.assertCountEqual(result, desired_result)
    
    if __name__ == "__main__":
        unittest.main()