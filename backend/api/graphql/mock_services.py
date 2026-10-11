from typing import BinaryIO

from core.interfaces.clients import AbstractS3Client


class MockS3Client(AbstractS3Client):
    async def get_file_size(self, bucket: str, key: str) -> int:
        return 1000

    async def generate_presigned_url(
        self,
        bucket: str,
        key: str,
        client_method: str,
        expires_in: int,
    ) -> str:
        return "generated_presigned_url"

    async def get_object(self, bucket: str, key: str) -> BinaryIO:
        return BinaryIO()

    async def put_object(self, bucket: str, key: str, file: BinaryIO) -> None:
        """
        Метод для загрузки файла в s3 хранилище.
        """

    async def delete_object(self, bucket: str, key: str) -> None:
        """
        Метод для удаления файла из s3 хранилища.
        """
