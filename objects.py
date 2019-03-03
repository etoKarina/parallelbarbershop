from threading import Thread, Lock, Event
import time, random

mutex = Lock()
# Interval in seconds
customerIntervalMin = 5
customerIntervalMax = 15
haircutDurationMin = 3
haircutDurationMax = 15


class Customer:

    def __init__(self, id, enterTime):
        self.id = id
        self.enterTime = enterTime


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
        print('{} на стрижке'.format(customer.id))
        randomHairCuttingTime = random.randrange(haircutDurationMin, haircutDurationMax + 1)
        # столько времени работает
        time.sleep(randomHairCuttingTime)
        print('{} подстрижен'.format(customer.id))


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
                print('Парикмахер спит')
                self.barber.sleep()
                print('Парикмахер не спит')

    def openShop(self):
        print('Парикмахерская открыта!')
        workingThread = Thread(target=self.barberGoToWork)
        workingThread.start()

    def enterBarberShop(self, customer):
        mutex.acquire()
        print('>> {} заходит и ищет место'.format(customer.id))

        if len(self.waitingCustomers) == self.numberOfSeats:
            print('Мест нет, {} уходит.'.format(customer.id))
            mutex.release()
        else:
            print('{} садится на место в зале ожидания'.format(customer.id))
            self.waitingCustomers.append(customer)
            mutex.release()
            self.barber.wakeUp()
