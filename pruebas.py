from threading import Timer

def hello():
    print ("hello, world")
    

Timer(2, hello).start() 
print("i came first")