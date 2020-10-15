#Enter a date and see what day was/is it.
date = (input('Date(DD-MM-YYYY)  = '))
date = date.split("-")
date
d = int(date[0])
m = int(date[1])
y = int(date[2])
n = [0,0,31,59,90,120,151,181,212,243,273,304,334,365]
m = n[m]

if (((y%4==0 and y%100!=0) or (y%400==0)) and (m<60)):
    day = ((y-1)*365+y//4-y//100+y//400+m+d-1)%7
else:
    day = ((y-1)*365+y//4-y//100+y//400+m+d)%7
days = ['Sunday','Monday','Tuesday','Wednessday','Thursday','Friday','Saturday']
print("Day   =",days[day])
