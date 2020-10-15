n = int(input("No. of Lines - "))
l = [0,1]
for i in range (1,n+1):
    m = [0,0]
    print(" "*(n-i)*(n//5),end = "")
    for j in range(i):
        x = l[j]+l[j+1]
        m.insert(len(m)-1,x)
        print(x,end = " "*(n//3))
    for i in range(n//10+1):
        print()
    l = m
