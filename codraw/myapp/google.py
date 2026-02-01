from google.cloud import storage
import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()


class Bucket:
    def __init__(self):
        client = storage.Client.from_service_account_json(
            os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
        self.bucket = client.bucket(os.getenv('GOOGLE_BUCKET'))

    def save(self, room, preview):
        blob = self.bucket.blob(f"{room}.webp")
        blob.upload_from_file(preview)

    def get_images(self, rooms):
        images = {}
        for room in rooms:
            blob = self.bucket.blob(f"{room}.webp")
            if blob.exists():
                images[room] = blob.generate_signed_url(
                    version="v4",
                    expiration=timedelta(minutes=15),
                    method="GET",
                )
        return images
