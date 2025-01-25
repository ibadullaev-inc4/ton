import asyncio
import requests
from pytonlib import TonlibClient
from pathlib import Path
from pytonlib.utils.tlb import Transaction, Slice, Cell, deserialize_boc
from tonsdk.utils import b64str_to_bytes



async def get_client(index):
    try:
        # url = 'https://ton.org/global-config.json'
        url = 'https://ton.org/testnet-global.config.json'
        config = requests.get(url).json()

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

async def main():
    client = await get_client(2)

    if not client:
        print("Не удалось создать клиента")
        return
    try:
        account_address = '0QC6BWNl1j9r4y78pxYMQpBK2fRQUAsLfbhitIKSJ0alix2C'
        txs = await client.get_transactions(account=account_address, limit=30)
        for tx in txs:
            cell = deserialize_boc(b64str_to_bytes(tx['data']))
            tx_data = Transaction(Slice(cell=cell))
            compute_ph = tx_data.description.compute_ph
            action_ph = tx_data.description.action
            if compute_ph.type == 'tr_phase_compute_vm':
                print('compute phase exit code is ', compute_ph.exit_code)
            if action_ph is not None:
                print('action phase exit code is ',action_ph.result_code)
    except Exception as e:
        print(f"Ошибка в main(): {e}")
    finally:
        await client.close()

if __name__ == '__main__':
    asyncio.run(main())
