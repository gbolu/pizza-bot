from tinydb import TinyDB, Query
import json, os

db = TinyDB(os.path.abspath('db.json'))
Order_Table = db.table('Order')

class Pizza():
    def __init__(self, toppings=None) -> None:
        self.toppings = toppings


class Order():
    """
    create an order 
    """
    def __init__(self, address=None, orderLocation=None, id=None, phone_no=None, possible_locations=None) -> None:
        self.orderStatus = "incomplete"
        self.address = address
        self.
        self.cart = []
        self.id = id
        self.phone_no = phone_no
        self.possible_locations = possible_locations

    @staticmethod
    def orderFromStore(order_dict: dict):
        """
        parameterized constructor
        """
        return Order(orderLocation=order_dict['orderLocation'], id=order_dict['id'], 
        phone_no=order_dict['phone_no'], possible_locations=order_dict['possible_locations'])

    def addToCart(self, item):
        self.cart.append(item)

    def addLocation(self, location):
        self.orderLocation = location

    def removeFromCart(self, item):
        self.cart.remove(item)

    def completeOrder(self):
        self.orderStatus = "complete"

    def store(self):
        User = Query()
        order_dict = json.loads(json.dumps(self.__dict__))
        if(Order_Table.get(User.id == self.id) == None):
            Order_Table.insert(order_dict)
        else:
            Order_Table.update(order_dict)

    @staticmethod
    def getOrder(id):
        User = Query()
        order = Order_Table.get(User.id == id)
        return json.loads(json.dumps(order))