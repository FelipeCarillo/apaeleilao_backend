import os
import boto3
import base64


class ImageManipulation:
    def __init__(self):
        self.__s3 = boto3.client('s3')
        self.__auction_folder = 'auctions/'
        self.__bucket = os.environ.get('BUCKET_NAME')

    def create_auction_folder(self, auction_id: str):
        try:
            auction_folder_key = f'{self.__auction_folder}{auction_id}/'
            self.__s3.put_object(ACL='public-read-write', Bucket=self.__bucket, Key=auction_folder_key, Body='')
        except Exception as e:
            raise e

    def upload_auction_image(self, auction_id: str, image_id: str, image_body: str, content_type: str):
        try:
            image_key = f'{self.__auction_folder}{auction_id}/{image_id}'
            self.__s3.put_object(ACL='public-read-write', Bucket=self.__bucket, Key=image_key, Body=base64.b64decode(image_body),
                                 ContentType=content_type)
            self.__auction_folder = f'{self.__auction_folder}{auction_id}/'
            return self.get_image_url(image_id)
        except Exception as e:
            raise e

    def delete_auction_image(self, image_name):
        pass

    def delete_auction_folder(self, auction_id):
        pass

    def get_image_url(self, image_id):
        return f"https://{self.__bucket}.s3.sa-east-1.amazonaws.com/" + self.__auction_folder + image_id
