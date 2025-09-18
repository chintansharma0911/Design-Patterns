from abc import ABC, abstractmethod
from typing import List


# --------------------------
# Models
# --------------------------

class MenuItem:
    def __init__(self, name: str, price: int, category: str):
        self.name = name
        self.price = price
        self.category = category

    def __repr__(self):
        return f"{self.name} ({self.category}) - ₹{self.price}"


class Restaurant:
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
        self.menu: List[MenuItem] = []

    def add_menu_item(self, item: MenuItem):
        self.menu.append(item)

    def __repr__(self):
        return f"Restaurant: {self.name} at {self.location}"


class Cart:
    def __init__(self, restaurant: Restaurant):
        self.restaurant = restaurant
        self.items: List[MenuItem] = []

    def add_to_cart(self, item: MenuItem):
        if item not in self.restaurant.menu:
            raise Exception("Item not available in this restaurant")
        self.items.append(item)

    def total_cost(self):
        return sum(item.price for item in self.items)

    def is_empty(self):
        return len(self.items) == 0

    def __repr__(self):
        return f"Cart({[item.name for item in self.items]})"


class User:
    def __init__(self, user_id: int, name: str, address: str):
        self.user_id = user_id
        self.name = name
        self.address = address
        self.cart: Cart | None = None


# --------------------------
# Singleton Managers
# --------------------------

class RestaurantManager:
    _instance = None

    def __init__(self):
        if RestaurantManager._instance is not None:
            raise Exception("Use get_instance()")
        self.restaurants: List[Restaurant] = []

    @staticmethod
    def get_instance():
        if RestaurantManager._instance is None:
            RestaurantManager._instance = RestaurantManager()
        return RestaurantManager._instance

    def add_restaurant(self, restaurant: Restaurant):
        self.restaurants.append(restaurant)

    def search_by_location(self, location: str):
        return [r for r in self.restaurants if r.location == location]


class OrderManager:
    _instance = None

    def __init__(self):
        if OrderManager._instance is not None:
            raise Exception("Use get_instance()")
        self.order_list: List['Order'] = []

    @staticmethod
    def get_instance():
        if OrderManager._instance is None:
            OrderManager._instance = OrderManager()
        return OrderManager._instance

    def add_order(self, order: 'Order'):
        self.order_list.append(order)

    def list_orders(self):
        return self.order_list


# --------------------------
# Payment Strategy
# --------------------------

class IPaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: int):
        pass


class CreditCardPayment(IPaymentStrategy):
    def pay(self, amount: int):
        print(f"Paid ₹{amount} via Credit Card.")


class NetBankingPayment(IPaymentStrategy):
    def pay(self, amount: int):
        print(f"Paid ₹{amount} via NetBanking.")


class UPIPayment(IPaymentStrategy):
    def pay(self, amount: int):
        print(f"Paid ₹{amount} via UPI.")


# --------------------------
# Orders
# --------------------------

class Order:
    def __init__(self, order_id: int, user: User, restaurant: Restaurant,
                 items: List[MenuItem], strategy: IPaymentStrategy):
        self.order_id = order_id
        self.user = user
        self.restaurant = restaurant
        self.items = items
        self.strategy = strategy

    def get_type(self):
        return "Generic Order"

    def place_order(self):
        if not self.items:
            raise Exception("Cart is empty!")
        total = sum(item.price for item in self.items)
        print(f"Placing order #{self.order_id} for {self.user.name}")
        self.strategy.pay(total)
        NotificationService(self).notify_user()
        OrderManager.get_instance().add_order(self)


class DeliveryOrder(Order):
    def __init__(self, order_id: int, user: User, restaurant: Restaurant,
                 items: List[MenuItem], strategy: IPaymentStrategy, address: str):
        super().__init__(order_id, user, restaurant, items, strategy)
        self.delivery_address = address

    def get_type(self):
        return "Delivery Order"


class PickupOrder(Order):
    def __init__(self, order_id: int, user: User, restaurant: Restaurant,
                 items: List[MenuItem], strategy: IPaymentStrategy, pickup_address: str):
        super().__init__(order_id, user, restaurant, items, strategy)
        self.pickup_address = pickup_address

    def get_type(self):
        return "Pickup Order"


# --------------------------
# Factories
# --------------------------

class IOrderFactory(ABC):
    @abstractmethod
    def create_order(self):
        pass


class ScheduleOrderFactory(IOrderFactory):
    def __init__(self, schedule_time: str):
        self.schedule_time = schedule_time

    def create_order(self, order: Order):
        print(f"Order scheduled at {self.schedule_time}")
        return order


class NowOrderFactory(IOrderFactory):
    def create_order(self, order: Order):
        print("Order placed immediately.")
        return order


# --------------------------
# Notification Service
# --------------------------

class NotificationService:
    def __init__(self, order: Order):
        self.order = order

    def notify_user(self):
        print(f"Notification: Your {self.order.get_type()} is confirmed!")


# --------------------------
# Demo
# --------------------------

if __name__ == "__main__":
    # Setup
    rm = RestaurantManager.get_instance()
    r1 = Restaurant("Dominos", "Delhi")
    r1.add_menu_item(MenuItem("Pizza", 250, "Main Course"))
    r1.add_menu_item(MenuItem("Coke", 50, "Beverage"))
    rm.add_restaurant(r1)

    user = User(1, "Alice", "Delhi")
    user.cart = Cart(r1)
    user.cart.add_to_cart(r1.menu[0])
    user.cart.add_to_cart(r1.menu[1])

    # Place Order
    payment = UPIPayment()
    order = DeliveryOrder(101, user, r1, user.cart.items, payment, user.address)
    factory = NowOrderFactory()
    final_order = factory.create_order(order)
    final_order.place_order()

    print("\nAll Orders:", OrderManager.get_instance().list_orders())
