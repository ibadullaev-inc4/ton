import asyncio
import requests
from pathlib import Path
from pytonlib import TonlibClient
import json


async def get_client(index):
    try:

        with open('./config.json') as f:
          config = json.loads(f.read())

        keystore_dir = '/tmp/ton_keystore'
        Path(keystore_dir).mkdir(parents=True, exist_ok=True)

        client = TonlibClient(
            ls_index=index,
            config=config,
            keystore=keystore_dir,
            tonlib_timeout=20
        )
        await client.init()
        return client
    except Exception as e:
        print(f"Ошибка при инициализации клиента: {e}")
        return None


async def get_block_txs(client: TonlibClient, wc, shard, seqno):
    try:
        result = await client.get_block_transactions(
            workchain=wc,
            shard=shard,
            seqno=seqno,
            count=40
        )
        return result['transactions']
    except Exception as e:
        print(f"Ошибка при получении транзакций блока: {e}")


async def main():
    client = await get_client(0)
    if not client:
        print("Не удалось создать клиента")
        return

    try:
        last_master_block = (await client.get_masterchain_info())['last']

        master_seqno = last_master_block['seqno']

        base_data = (await client.get_shards(master_seqno=master_seqno))['shards'][0]

        base_shard = base_data['shard']
        base_seqno = base_data['seqno']
        base_workchain = base_data['workchain']

        txs = await get_block_txs(client=client,wc=base_workchain,shard=base_shard,seqno=base_seqno)

        for tx in txs:
            full_tx = await client.get_transactions(account=tx['account']\
              ,from_transaction_lt=tx['lt']\
              ,from_transaction_hash=tx['hash'])
            print(full_tx)

    except Exception as e:
        print(f"Ошибка в main(): {e}")
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.run(main())
