def fungsi (jenis,x,y):
	try:
		if (jenis=='MUL'):
			return int(x)*int(y)
		elif (jenis=='ADD'):
			return int(x)+int(y)
		elif (jenis=='SUB'):
			return int(x)-int(y)
		else:
			return 'ERR'
	except ValueError:
		return 'ERROR'
