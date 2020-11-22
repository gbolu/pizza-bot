class Pizza():
    def __init__(self, toppings=None) -> None:
        self.toppings = toppings


class Order():
    """
    create an order 
    """
    def __init__(self, location=None) -> None:
        self.orderStatus = "incomplete"
        self.orderLocation = location
        self.cart = []

    def addToCart(self, item):
        self.cart.append(item)

    def addLocation(self, location):
        self.orderLocation = location

    def removeFromCart(self, item):
        self.cart.remove(item)

    def completeOrder(self):
        self.orderStatus = "complete"