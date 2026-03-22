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

    def save(self, room: str, preview: str, title: str | None = None) -> None:
        title = title or room
        blob = self.bucket.blob(f"{room}/{self.stringify_title(title)}.png")
        blob.upload_from_file(preview)

    def get_images(self, rooms: list) -> dict:
        images = {}
        for room in rooms:
            blobs = list(self.bucket.list_blobs(prefix=f"{room}/"))
            if blobs:
                blob = blobs[0]
                title = blob.name.split("/")[-1]
                images[room] = blob.generate_signed_url(
                    version="v4",
                    expiration=timedelta(minutes=15),
                    method="GET",
                    response_disposition=f"attachment; filename*=UTF-8'{
                        title}'",
                )
        return images

    @staticmethod
    def stringify_title(title: str) -> str:
        title.replace(" ", "-")
        return title
