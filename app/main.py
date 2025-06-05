import os
import asyncio
from random import randint
from dotenv import load_dotenv

from meross import MerossConnection

# Load environment variables
load_dotenv()


async def main():
    # Initialise connection to Meross API
    meross_conn = MerossConnection(
        meross_email=os.getenv("MEROSS_EMAIL"), 
        meross_password=os.getenv("MEROSS_PASSWORD")
    )
    await meross_conn.connect()

    # Discover devices
    smart_lamps = meross_conn.manager.find_devices(device_type="msl430")

    if len(smart_lamps) >= 1:
        device = smart_lamps[0]

        # Update device status: this is needed only once or if the connection goes down
        await device.async_update()

        if device.get_supports_rgb():
            # Check the current RGB color
            current_color = device.get_rgb_color()
            print(f"Current color of {device.name}: {current_color}")

            # Set a random RGB color
            rgb = randint(0, 255), randint(0, 255), randint(0, 255)
            await device.async_set_light_color(rgb=rgb)
            print(f"Updated colour of {device.name} to {rgb}")

            await asyncio.sleep(5)

            # Return to the original color
            await device.async_set_light_color(rgb=current_color)
            print(f"Returned {device.name} to {current_color}")
        else:
            print(f"Unfortunately, {device.name} does not support RGB...")
    else:
        print("No smart lamps found...")

    # Close the manager and logout from http_api
    await meross_conn.disconnect()


if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy())
    
    # Automatically create and manage loops
    asyncio.run(main())
