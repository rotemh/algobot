import base64
from algosdk import transaction

class Contract(object):
    def __init__(self, algod):
        self.algod = algod

    def execute(self, address, station, temperature):
        program = base64.b64decode(
            "ASAG0A8BAAWo7Y0CUCYCIPQv9Dp6BUP5IWgVnUMxQ41GHJYlTMUn5MaVgxmacIXBIHiNgRcdCvcgzeloO+LUHFaqn/aCtb6wV9B8WJqe5FcWMQEiDDEQIxIQMQgkEhAxCSgSMQcyAxIQLRclEhAxAiEEDhAuFyEFDhAxCSkSMQcyAxIQMQIhBA0uFyEFDREQERA=")

        lsig = transaction.LogicSig(program, args=[[station], [temperature]])
        sender = lsig.address()

        # get suggested parameters
        params = self.algod.suggested_params()
        gh = params["genesishashb64"]
        last_round = params["lastRound"]
        fee = params["fee"]

        txn = transaction.PaymentTxn(sender, fee, last_round, last_round + 1000, gh,
                                     "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY5HFKQ", 0,
                                     close_remainder_to=address)

        # note, transaction is signed by logic only (no delegation)
        # that means sender address must match to program hash
        lstx = transaction.LogicSigTransaction(txn, lsig)
        assert lstx.verify()

        # send them over network
        return self.algod.send_transaction(lstx, headers={'content-type': 'application/x-binary'})
