import bank as b

testBank = b.Bank()
newUser = testBank.create_user("Rudra","rudra@gmail.com")
secondUser = testBank.create_user("Bob","Bob@gmail.com")

testBank.deposit(user_id=newUser.id,amount=100)
testBank.deposit(user_id=secondUser.id,amount=100)

testBank.request_transfer(sender_id=newUser.id, receiver_id=secondUser.id, transaction_amount=50)


print(testBank.transactions)