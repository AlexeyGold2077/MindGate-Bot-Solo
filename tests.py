import mindgate

print('getBalance - ', mindgate.getBalance(123))
print('addBalance - ', mindgate.addBalance(123, 1000))
print('getBalance - ', mindgate.getBalance(123))
print('sendMessageAsSystem - ', mindgate.sendMessageAsSystem(123, "be very breif"))
print('sendMessageAsUser - ', mindgate.sendMessageAsUser(123, "hi"))
print('getBalance - ', mindgate.getBalance(123))
print('sendMessageAsUser - ', mindgate.sendMessageAsUser(123, "напиши очень короткий стих"))
print('getBalance - ', mindgate.getBalance(123))
print('clearMessages - ', mindgate.clearMessages(123))
print('getModel - ', mindgate.getModel(123))
print('setModel - ', mindgate.setModel(123, "gpt-4o"))
print('getModel - ', mindgate.getModel(123))
