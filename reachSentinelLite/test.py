try:
    while True:
		person = input('Enter your name: ')
		print('Hello ' + person)
except KeyboardInterrupt:
    print('interrupted!')