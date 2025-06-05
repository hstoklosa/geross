import os
from dotenv import load_dotenv

import asyncio
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

# Load environment variables
load_dotenv()


async def main():
    client = await MerossHttpClient.async_from_user_password(
        email=os.getenv("MEROSS_EMAIL"), 
        password=os.getenv("MEROSS_PASSWORD"), 
        api_base_url="https://iot.meross.com"
    )

    # Setup and start the device manager
    manager = MerossManager(http_client=client)
    await manager.async_init()

    # Discover devices
    await manager.async_device_discovery()
    smart_lamp = manager.find_devices(device_type="msl430")

    print(smart_lamp[0].name)

    # Close the manager and logout from http_api
    manager.close()
    await client.async_logout()


if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy())
        
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.stop()
