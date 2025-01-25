import asyncio
from TonTools import Wallet, TonApiClient, TonCenterClient, LsClient

async def main():

    # client = TonApiClient()
    
    # client = TonCenterClient(base_url='http://127.0.0.1:8801/')

    # client = TonCenterClient(orbs_access=True,testnet=True)

    client = LsClient(ls_index=2, default_timeout=30, addresses_form='user_friendly')
    await client.init_tonlib()

    mnemonics = ['trigger', 'eagle', 'enough', 'sauce', 'chalk', 'voyage', 'endless', 'vacuum', 'abstract', 'denial', 'matter', 'appear', 'cute', 'joke', 'together', 'blur', 'sand', 'cotton', 'echo', 'erode', 'nasty', 'voyage', 'twice', 'lava']
    wallet = Wallet(mnemonics=mnemonics,provider=client)

    # to_addr = '0QCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqPvC'
    # await wallet.get_seqno()

    print(await wallet.get_transactions(5))  

    # await wallet.transfer_ton(destination_address=to_addr, amount=100, send_mode=0)

if __name__ == '__main__':
    asyncio.run(main())



