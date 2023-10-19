import os
import boto3


class ImageManipulation:
    def __init__(self):
        self.__bucket = os.environ.get('BUCKET_NAME')
        self.__client = boto3.client('s3')
        self.__auction_folder = 'auctions/'

    def create_folder(self, folder_name):
        try:
            response = self.__client.put_object(
                Bucket=self.__bucket,
                Key=folder_name
            )
            return response['ResponseMetadata']['HTTPStatusCode'] == 200
        except Exception as e:
            raise e

    def upload_auction_image(self, auction_id: str, image_id: str, image_body: str):
        try:
            image_bytes = image_body.encode('utf-8')
            response = self.create_folder(auction_id)
            if not response:
                raise Exception('Erro ao criar pasta de imagens para o leilão.')
            response = self.__client.put_object(
                Body=image_bytes,
                Bucket=self.__bucket + '/' + self.__auction_folder + auction_id,
                Key=image_id,
                ACL='public-read'
            )
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise Exception('Erro ao fazer upload da imagem.')
            folder_name = self.__auction_folder + auction_id
            return self.get_image_url(self.__bucket, folder_name, image_id)
        except Exception as e:
            raise e

    def delete_auction_image(self, image_name):
        self.__client.delete_object(
            Bucket='apaeleilao-images',
            Key=image_name
        )

    @staticmethod
    def get_image_url(bucket_name, folder_name, image_name):
        return f"https://{bucket_name}.s3.sa-east-1.amazonaws.com/" + folder_name + image_name
