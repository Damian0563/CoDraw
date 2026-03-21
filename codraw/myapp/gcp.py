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

    def save(self, room: str, preview: str, title: str | None = None):
        blob = self.bucket.blob(f"{room}.png")
        if not title:
            title = blob.metadata.get('title', room)
        blob.upload_from_file(preview)
        blob.metadata = {'title': title}
        blob.patch()

    def get_images(self, rooms: list):
        images = {}
        for room in rooms:
            blob = self.bucket.blob(f"{room}.png")
            if blob.exists():
                title = blob.metadata.get('title', room)
                images[room] = blob.generate_signed_url(
                    version="v4",
                    expiration=timedelta(minutes=15),
                    method="GET",
                    response_disposition=f'attachment; filename="{title}.png"',
                )
        return images
