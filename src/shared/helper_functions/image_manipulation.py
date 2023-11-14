import os
import boto3
import base64


class ImageManipulation:
    def __init__(self):
        self.__bucket = os.environ.get('BUCKET_NAME')
        self.__s3 = boto3.resource('s3')
        self.__auction_folder = 'auctions/'

    def create_auction_folder(self, auction_id: str):
        try:
            Object = self.__s3.Object(self.__bucket, self.__auction_folder)
            self.__auction_folder = self.__auction_folder + auction_id + "/"
            Object.put(self.__auction_folder)
        except Exception as e:
            raise e

    def upload_auction_image(self, image_id: str, image_body: str, content_type: str):
        try:
            Bucket = self.__s3.Object(self.__bucket, self.__auction_folder + image_id + "." + content_type)
            Bucket.put(Body=base64.b64decode(image_body))
            return self.get_image_url(image_id)
        except Exception as e:
            raise e

    def delete_auction_image(self, image_name):
        pass

    def get_image_url(self, image_id):
        return f"https://{self.__bucket}.s3.sa-east-1.amazonaws.com/" + self.__auction_folder + image_id
