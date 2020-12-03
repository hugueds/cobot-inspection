from threading import Thread
from time import sleep

class A:
    p1 = 0

class B:
    p1 = 0        

    def start_thread(self, a: A):        
        self.active_thread = True
        self.thread = Thread(target=self.increment, args=(a,), daemon=True)
        self.thread.start()        

    def increment(self, a: A):
        while self.active_thread:
            print('Increment thread')
            a.p1 += 1
            sleep(1)

    def stop_thread(self):
        self.active_thread = False       


def main():
    a_instance = A()
    b_instance = B()
    b_instance.start_thread(a_instance)
    i = 0
    while True:        
        print('p1 value :', a_instance.p1)
        i += 1
        if i > 3:
            b_instance.stop_thread()
        sleep(3)

    print('End loop')


  

if __name__ == '__main__':
    try:
        main()        
    except Exception as e:
        print('Finishing program due error')
        print(e)
