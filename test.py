import database as Database

me = Database("users", "hillcrestpaul0719")
try:
    print(me.variables['password'])
except:
    pass
me.variables['password'] = "newPassword"
me.save()
