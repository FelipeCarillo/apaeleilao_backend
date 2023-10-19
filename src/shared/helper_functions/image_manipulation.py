import os
import boto3


class ImageManipulation:
    def __init__(self):
        self.__bucket = os.environ.get('BUCKET_NAME')
        self.__client = boto3.client('s3')
        self.__auction_folder = 'auctions/'

    def upload_auction_image(self, image: Image):
        image_bytes = image.encode('utf-8')
        self.__client.put_object(
            Body=image_bytes,
            Bucket=self.__bucket + '/',
            Key=image_name,
            ACL='public-read'
        )
        return self.get_auction_image_url(self.__auction_folder, image_name)

    def delete_auction_image(self, image_name):
        self.__client.delete_object(
            Bucket='apaeleilao-images',
            Key=image_name
        )

    def get_image_url(self, folder_name, image_name):
        return f"https://{self.__bucket}.s3.sa-east-1.amazonaws.com/" + folder_name + image_name
