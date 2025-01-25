import asyncio
import aiohttp
from pathlib import Path
from pytonlib import TonlibClient
import logging

logging.basicConfig(level=logging.DEBUG)

async def fetch_config():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://ton.org/global.config.json') as response:
            return await response.json()

async def main():
    # downloading mainnet config asynchronously
    ton_config = await fetch_config()

    # create keystore directory for tonlib
    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    # init TonlibClient
    client = TonlibClient(
        ls_index=0,  # choose LiteServer index to connect
        config=ton_config,
        keystore=keystore_dir
    )

    try:
        await client.init()
        # masterchain_info = await client.get_masterchain_info()
        # print(masterchain_info)
        # block_header = await client.get_block_header(**masterchain_info['last'])
        # print(block_header)
        # shards = await client.get_shards(master_seqno=masterchain_info['last']['seqno'])
        # print(shards)
    except asyncio.CancelledError:
        logging.error("Task was cancelled.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Running the main async function
asyncio.run(main())
