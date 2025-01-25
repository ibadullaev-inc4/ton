import requests
import asyncio
import json
from pathlib import Path
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from tonsdk.utils import to_nano


from pytonlib import TonlibClient


async def get_seqno(client: TonlibClient, address: str):
    data = await client.raw_run_method(method='seqno', stack_data=[], address=address)
    return int(data['stack'][0][1], 16)


async def main():

    mnemonics = ['trigger', 'eagle', 'enough', 'sauce', 'chalk', 'voyage', 'endless', 'vacuum', 'abstract', 'denial', 'matter', 'appear', 'cute', 'joke', 'together', 'blur', 'sand', 'cotton', 'echo', 'erode', 'nasty', 'voyage', 'twice', 'lava']
    mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(mnemonics=mnemonics ,version=WalletVersionEnum.v3r2, workchain=0)
    wallet_address = wallet.address.to_string(True, True, True, True)
    # print(mnemonics)
    # print(wallet.address.to_string(True, True, True, True))

    

    loop = asyncio.get_running_loop()
    ton_config = requests.get('https://ton.org/testnet-global.config.json').json()


    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)
    
    client = TonlibClient(ls_index=12,
                          config=ton_config,
                          keystore=keystore_dir,
                          loop=loop, tonlib_timeout=15)
    
    await client.init()
    
    # masterchain_info = await client.get_masterchain_info()
    # block_header = await client.get_block_header(**masterchain_info['last'])
    # print(json.dumps(block_header, indent=4))


    query = wallet.create_init_external_message()
    deploy_message = query['message'].to_boc(False)
    # print(await client.raw_run_method(method='seqno', stack_data=[],address=wallet_address))



    seqno = await get_seqno(client, wallet_address)
    # print(seqno)

    transfer_query = wallet.create_transfer_message(to_addr='0QCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqPvC',
                                   amount=to_nano(10.01, 'ton'), seqno=seqno, payload='test message for check transfer')
                                

    transfer_message = transfer_query['message'].to_boc(False)


    await client.raw_send_message(transfer_message)

    # await client.raw_send_message(deploy_message)



    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
    # asyncio.get_event_loop().run_until_complete(main())
