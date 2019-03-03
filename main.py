from objects import BarberShop, Barber, Customer
from objects import customerIntervalMin, customerIntervalMax
import time, random

# hi Karina

if __name__ == "__main__":
    customers = [Customer(0), Customer(1), Customer(2), Customer(3), Customer(4), Customer(5), ]
    barber = Barber()
    barShop = BarberShop(barber, numberOfSeats=2)
    barShop.openShop()
    while len(customers) > 0:
        c = customers.pop()
        # New customer enters the barbershop
        barShop.enterBarberShop(c)
        customerInterval = random.randrange(customerIntervalMin, customerIntervalMax + 1)
        time.sleep(customerInterval)
