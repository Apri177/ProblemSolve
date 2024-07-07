n, m, h = map(int,input().split())

ans = 0

while n != 0:

	n -= 1

	# 제2사분면
	if m < 2 ** n and h < 2 ** n:
		ans += ( 2 ** n ) * ( 2 ** n ) * 0

	# 제1사분면
	elif m < 2 ** n and h >= 2 ** n: 
		ans += ( 2 ** n ) * ( 2 ** n ) * 1
		h -= ( 2 ** n )
        
	# 제3사분면    
	elif m >= 2 ** n and h < 2 ** n: 
		ans += ( 2 ** n ) * ( 2 ** n ) * 2
		m -= ( 2 ** n )
        
	# 제4사분면    
	else:
		ans += ( 2 ** n ) * ( 2 ** n ) * 3
		m -= ( 2 ** n )
		h -= ( 2 ** n )
    
print(ans)