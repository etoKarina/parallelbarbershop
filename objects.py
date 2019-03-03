from threading import Thread, Lock, Event
import time, random

mutex = Lock()
# Interval in seconds
customerIntervalMin = 5
customerIntervalMax = 15
haircutDurationMin = 3
haircutDurationMax = 15


class Customer:
    def __init__(self, id):
        self.id = id


class Barber:
    barberWorkingEvent = Event()

    def sleep(self):
        # процесс ждет пока его вызовут
        self.barberWorkingEvent.wait()

    def wakeUp(self):
        # Подготовить процесс для принятия
        self.barberWorkingEvent.set()

    def cutHair(self, customer):
        # Установить состояние процесса
        self.barberWorkingEvent.clear()
        print('{} is having a haircut'.format(customer.id))
        randomHairCuttingTime = random.randrange(haircutDurationMin, haircutDurationMax + 1)
        # столько времени работает
        time.sleep(randomHairCuttingTime)
        print('{} is done'.format(customer.id))


class BarberShop:
    waitingCustomers = []

    def __init__(self, barber, numberOfSeats):
        self.barber = barber
        self.numberOfSeats = numberOfSeats

    def barberGoToWork(self):
        while True:
            mutex.acquire()

            if len(self.waitingCustomers) > 0:
                c = self.waitingCustomers[0]
                del self.waitingCustomers[0]
                mutex.release()
                self.barber.cutHair(c)
            else:
                mutex.release()
                print('Aaah, all done, going to sleep')
                self.barber.sleep()
                print('Barber woke up')

    def openShop(self):
        print('Barber shop is opening')
        workingThread = Thread(target=self.barberGoToWork)
        workingThread.start()

    def enterBarberShop(self, customer):
        mutex.acquire()
        print('>> {0} entered the shop and is looking for a seat'.format(customer.id))

        if len(self.waitingCustomers) == self.numberOfSeats:
            print('Waiting room is full, {0} is leaving.'.format(customer.id))
            mutex.release()
        else:
            print('{0} sat down in the waiting room'.format(customer.id))
            self.waitingCustomers.append(customer)
            mutex.release()
            self.barber.wakeUp()
