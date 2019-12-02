from algosdk import algod, transaction, mnemonic, account, encoding
import json


class DeliveryGuy(object):
    def __init__(self, algod, passphrase,
                 namespace_address="X6E3EZE53KAJRPUWPRLRPRDIGIFIUUVB67LJ4RBA73GJDL5N7DRQ466RAM"):
        self.algod = algod
        self.namespace_address = namespace_address
        self.sk = mnemonic.to_private_key(passphrase)

    def track(self, station: int, temperature: int):
        """
        posts the tracking information to the blockchain
        :param station:
        :param temperature:
        :return:
        """

        # get suggested parameters
        params = self.algod.suggested_params()
        gen = params["genesisID"]
        gh = params["genesishashb64"]
        last_round = params["lastRound"]
        fee = params["fee"]

        note = {
            's': station,
            't': temperature
        }

        # create the transaction
        txn = transaction.PaymentTxn(account.address_from_private_key(self.sk), fee, last_round, last_round + 1000, gh,
                                     self.namespace_address, 0, note=json.dumps(note).encode())

        # sign it
        stx = txn.sign(self.sk)

        # send it
        return self.algod.send_transaction(stx, headers={'content-type': 'application/x-binary'})


# Driver
def main():
    acl = algod.AlgodClient("", "https://testnet-algorand.api.purestake.io/ps1",
                            headers={"X-API-Key": "", })

    passphrase = "clutch amazing lizard fault hub melody consider latin slab index guide giant cheap found only cradle noodle syrup sister coach fuel title biology absorb almost"

    dg = DeliveryGuy(acl, passphrase)

    dg.track(3, 82)


if __name__ == '__main__':
    main()
