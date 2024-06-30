from twilio.rest import Client

account_sid = 'AC6504c9a4faf6d219e6fac693ecf015cc'
auth_token = '8f1cbfe841c7d32a1646e7185f86e527'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='Your appointment is coming up on July 21 at 3PM',
  to='whatsapp:+6283861367245'
)

print(message.sid)