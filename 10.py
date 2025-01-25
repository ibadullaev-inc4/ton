import asyncio
import requests
from pytonlib import TonlibClient
from pathlib import Path
from pytonlib.utils.tlb import Transaction, Slice, Cell, deserialize_boc, CommentMessage, JettonTransferNotificationMessage
from tonsdk.utils import b64str_to_bytes
import json

async def get_client():
    try:
        with open('./config.json') as f:
          config = json.loads(f.read())

        keystore_dir = '/tmp/ton_keystore'
        Path(keystore_dir).mkdir(parents=True, exist_ok=True)

        client = TonlibClient(
            ls_index=0,
            config=config,
            keystore=keystore_dir,
            tonlib_timeout=20
        )
        await client.init()
        return client
    except Exception as e:
        print(f"Ошибка при инициализации клиента: {e}")
        return None

async def main():

    client = await get_client()
    if not client:
        return

    try:
        last_master_block = (await client.get_masterchain_info())['last']
        master_seqno = last_master_block['seqno']

        base_data = (await client.get_shards(master_seqno=master_seqno))['shards'][0]
        print(base_data)

        base_shard = base_data['shard']
        base_seqno = base_data['seqno']
        base_workchain = base_data['workchain']

        txs = (await client.get_block_transactions(workchain=base_workchain,shard=base_shard,seqno=base_seqno,count=10))['transactions']
        for tx in txs:
            print(tx)
    except Exception as e:
        print(f"Ошибка в main(): {e}")
    finally:
        await client.close()

if __name__ == '__main__':
    asyncio.run(main())
