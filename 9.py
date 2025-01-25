import asyncio
import requests
from pytonlib import TonlibClient
from pathlib import Path
from pytonlib.utils.tlb import Transaction, Slice, Cell, deserialize_boc, CommentMessage, JettonTransferNotificationMessage
from tonsdk.utils import b64str_to_bytes
import json


async def get_client(index):
    try:
        # # url = 'https://ton.org/global-config.json'
        # url = 'https://ton.org/testnet-global.config.json'
        # config = requests.get(url).json()

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

async def main():

    # message = "AAAAAHRoYW5rIHlvdSBmb3IgbW9uZnk="
    # cell = Cell()
    # cell.data.from_bytes(b64str_to_bytes(message))
    # result = CommentMessage.parse(Slice(cell=cell))
    # print(cell.data.data.to01())
    # print(result.text_comment)

    client = await get_client(0)

    if not client:
        print("Не удалось создать клиента")
        return
    try:
        txs = await client.get_transactions(account='UQBYnnsOcO0m5Gj3WUgs7l5YH1WUbtzhaXvyfXxQ3vF6la8-', limit=10)
        for tx in txs:
            try:
                body = tx['in_msg']['msg_data']['body']
                print(body)
                cell = deserialize_boc(b64str_to_bytes(body))
                result = JettonTransferNotificationMessage(Slice(cell=cell))
                print(result)
                sender_address = Address(str(result.sender.workchain_id) + ':' + str(result.sender.address)).to_string(True, True, True)
                print(result.amount, sender_address)
            except:
                pass

    except Exception as e:
        print(f"Ошибка в main(): {e}")
    finally:
        await client.close()

if __name__ == '__main__':
    asyncio.run(main())
