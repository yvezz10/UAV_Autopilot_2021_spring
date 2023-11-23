import datetime
import time

today = datetime.date.today()
target = today + datetime.timedelta(days = 13)
label = "%04d/%02d/%02d" %(target.year ,target.month ,target.day)

print(label)