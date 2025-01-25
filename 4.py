import asyncio
import requests
from pathlib import Path
from pytonlib import TonlibClient

async def transactions():
    url = 'https://ton.org/global-config.json'
    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=2, config=config, keystore=keystore_dir, tonlib_timeout=30)

    await client.init()

    account = 'UQBYnnsOcO0m5Gj3WUgs7l5YH1WUbtzhaXvyfXxQ3vF6la8-'
    limit = 10
    transactions = await client.get_transactions(account=account, limit=limit)

    for tx in transactions:
        tx_id = tx.get("transaction_id", {})
        address = tx.get("address", {}).get("account_address", "Неизвестно")
        utime = tx.get("utime", "Неизвестно")
        fee = tx.get("fee", "Неизвестно")
        lt = tx_id.get("lt", "Неизвестно")
        hash_ = tx_id.get("hash", "Неизвестно")
        
        print(f"Адрес: {address}")
        print(f"Время транзакции: {utime}")
        print(f"Fee: {fee}")
        print(f"LT: {lt}")
        print(f"Hash: {hash_}")
        print("-" * 50)

    # Завершение работы клиента
    await client.close()

if __name__ == '__main__':
    asyncio.run(transactions())
