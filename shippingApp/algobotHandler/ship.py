from pyteal import *

""" 
/ Money is released under two circumstances:
// 1. To SELLER if arg0 == FINAL_DEST && txn.FirstValid <= TIMEOUT && TEMP <= 80
// 2. To BUYER if txn.FirstValid > TIMEOUT || TEMP >80
"""
buyer = Addr("PCGYCFY5BL3SBTPJNA56FVA4K2VJ75UCWW7LAV6QPRMJVHXEK4LJHYKKKE")
seller = Addr("6QX7IOT2AVB7SILICWOUGMKDRVDBZFRFJTCSPZGGSWBRTGTQQXA56NOWNA")
max_temp = 80
last_station = 5
timeout = 4421288
max_fee = 2000

fee_cond = Txn.fee() < Int(max_fee)
type_cond = Txn.type_enum() == Int(1)
amount_cond = Txn.amount() == Int(0)
success_cond = And(Txn.close_remainder_to() == seller,
             Txn.receiver() == Global.zero_address(),
             Btoi(Arg(0)) == Int(last_station),
             Txn.first_valid() <= Int(timeout),
             Btoi(Arg(1)) <= Int(max_temp))
fail_cond = And(Txn.close_remainder_to() == buyer,
                Txn.receiver() == Global.zero_address(),
                (Txn.first_valid() > Int(timeout)).Or(Btoi(Arg(1)) > Int(max_temp)))

ship = fee_cond.And(type_cond).And(amount_cond).And(success_cond.Or(fail_cond))

print(ship.teal())