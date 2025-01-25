import asyncio
import requests
from pathlib import Path
from pytonlib import TonlibClient


async def get_client(index):
    url = 'https://ton.org/global-config.json'
    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=index, config=config, keystore=keystore_dir, tonlib_timeout=20)

    await client.init()

    return client

async def get_block_txs(client: TonlibClient ,wc ,shard ,seqno ):
    await client.get_block_transactions(workchain=wc, shard=shard, seqno=seqno, count=40)


async def main():
    client = await get_client(2)
    print(await client.get_masterchain_info())

    # await get_block_txs()


if __name__ == '__main__':
    asyncio.run(main())
