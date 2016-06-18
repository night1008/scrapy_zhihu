#conding: utf-8

def login():
	print 'login'

def log(f):
	def __decorate():
		print 'before log'
		f()
		print 'after log'
	return __decorate

login_with_log = log(login)


if __name__ == '__main__':
	# login_with_log()
	def printdebug(func):
	    def __decorator(user):    #add parameter receive the user information
	        print('enter the login')
	        func(user)  #pass user to login
	        print('exit the login')
	    return __decorator  
 
	@printdebug 
	def login(user):
	    print('in login:' + user)
	 
	login('jatsz')  #arguments:jatsz