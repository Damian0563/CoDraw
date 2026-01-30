from google.cloud import storage
from google.oauth2 import service_account
import os
from dotenv import load_dotenv
load_dotenv()


class Bucket:
    def __init__(self):
        client = storage.Client.from_service_account_json(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
        self.bucket = client.get_bucket(os.getenv('GOOGLE_BUCKET'))
    def save(self,room,preview):
        blob = self.bucket.blob(f"{room}.webp")
        blob.upload_from_string(preview)
