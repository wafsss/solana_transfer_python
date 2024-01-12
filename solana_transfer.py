# -*- coding: utf-8 -*-

from solana.transaction import Transaction
from solders.keypair import Keypair
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams
from key import privatekey


#这个函数用于发送SOL（Solana的原生代币）到指定的公钥地址。  它接受4个参数：
#url（Solana RPC节点的URL），privatekey（发送者的私钥），to_pubkey（接收者的公钥），
#和amount（要发送的SOL数量，以lamports为单位，1 SOL = 10^9 lamports）。

#难点就是在于如何构建交易
def send_sols(url,privatekey,to_pubkey,amount):
    #创建一个Client实例，用于与Solana RPC API进行通信
    client = Client(url)

    #从私钥创建一个Keypair实例，然后从中获取公钥
    payer_keypair = Keypair.from_base58_string(privatekey)
    payer_pubkey = payer_keypair.pubkey()
    print("Public key: {}".format(payer_pubkey))

    #构建一个TransferParams实例，它包含了转账的相关信息
    it_transfer = transfer(TransferParams(
        from_pubkey=payer_pubkey,
        to_pubkey=Pubkey.from_base58_string(to_pubkey),
        lamports=amount,
    ))
    print(it_transfer)

    #获取最新的区块哈希值
    result = client.get_latest_blockhash()
    #将区块哈希值设置为交易的recent_blockhash属性
    blockhash = result.value.blockhash

    #创建一个Transaction实例，然后将转账交易添加到其中
    tx = Transaction(recent_blockhash=blockhash,fee_payer=payer_pubkey)
    tx.add(it_transfer)

    #使用客户端的send_transaction方法发送交易
    hash = client.send_transaction(tx,payer_keypair)
    print(hash.value)


if  __name__ == '__main__':
    url = "https://api.devnet.solana.com"
    #设置接收者的公钥和一个转账金额（这里是1 SOL，转换为lamports是1000000000）
    #privatekey = privatekey
    to_pubkey = "4k3fT8vg9QGKZWGqNVTuW592DK3oHtQ7qQ4QKm"
    amount = 1000000000
    #调用send_sols函数发送SOL
    send_sols(url,privatekey,to_pubkey,amount)
















