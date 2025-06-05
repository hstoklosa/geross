import asyncio
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager


class MerossConnection:
    """A class to handle the connection to Meross API."""

    def __init__(self, meross_email, meross_password):
        self.meross_email = meross_email
        self.meross_password = meross_password
        self.meross_api_base_url = "https://iot.meross.com"
        self.event_loop = asyncio.get_event_loop()
        self.client = None
        self.manager = None

    async def connect(self):
        try:
            self.client = await MerossHttpClient.async_from_user_password(
                email=self.meross_email, 
                password=self.meross_password, 
                api_base_url=self.meross_api_base_url
            )
            self.manager = MerossManager(http_client=self.client)
            await self.manager.async_init()
            await self.manager.async_device_discovery()
        except Exception as e:
            print(f"Error connecting to Meross: {e}")
            self.client = None
            self.manager = None

    async def disconnect(self):
        try:
            self.manager.close()
            await self.client.async_logout()
        except Exception as e:
            print("Error terminating Meross Connection: {e}")
            self.manager = None
            self.client = None
