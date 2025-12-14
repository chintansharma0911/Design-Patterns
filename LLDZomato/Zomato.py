from abc import ABC, abstractmethod
from typing import List


class MenuItem:
    def __init__(self, code: str, name: str, price: int):
        self.code = code
        self.name = name
        self.price = price


class Restaurant:
    def __init__(self, restaurant_id: int, name: str, location: str):
        self.restaurant_id = restaurant_id
        self.name = name
        self.location = location
        self.menu_items: List[MenuItem] = []

    def add_menu_item(self, item: MenuItem):
        self.menu_items.append(item)


class Cart:
    def __init__(self, user):
        self.user = user
        self.items: List[MenuItem] = []

    def add_to_cart(self, item: MenuItem):
        self.items.append(item)

    def total_cost(self):
        return sum(item.price for item in self.items)

    def is_empty(self):
        return len(self.items) == 0


class User:
    def __init__(self, user_id: int, name: str, address: str):
        self.user_id = user_id
        self.name = name
        self.address = address
        self.cart = Cart(self)


class RestaurantManager:
    _instance = None

    def __init__(self):
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
        self.orders = []

    @staticmethod
    def get_instance():
        if OrderManager._instance is None:
            OrderManager._instance = OrderManager()
        return OrderManager._instance

    def add_order(self, order):
        self.orders.append(order)

    def list_orders(self):
        return self.orders


class IPaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: int):
        pass


class CreditCardPayment(IPaymentStrategy):
    def pay(self, amount: int):
        print(f"Paid ₹{amount} using Credit Card")


class NetBankingPayment(IPaymentStrategy):
    def pay(self, amount: int):
        print(f"Paid ₹{amount} using Net Banking")


class UPIPayment(IPaymentStrategy):
    def pay(self, amount: int):
        print(f"Paid ₹{amount} using UPI")


class Order(ABC):
    def __init__(self, order_id: int, user: User, restaurant: Restaurant, items: List[MenuItem]):
        self.order_id = order_id
        self.user = user
        self.restaurant = restaurant
        self.items = items
        self.payment_strategy: IPaymentStrategy = None

    def set_payment_strategy(self, strategy: IPaymentStrategy):
        self.payment_strategy = strategy

    def total_cost(self):
        return sum(item.price for item in self.items)

    def pay(self):
        if not self.payment_strategy:
            raise Exception("Payment strategy not set")
        self.payment_strategy.pay(self.total_cost())

    @abstractmethod
    def get_type(self):
        pass


class DeliveryOrder(Order):
    def __init__(self, order_id, user, restaurant, items, delivery_address):
        super().__init__(order_id, user, restaurant, items)
        self.delivery_address = delivery_address

    def get_type(self):
        return "DELIVERY"


class PickupOrder(Order):
    def __init__(self, order_id, user, restaurant, items):
        super().__init__(order_id, user, restaurant, items)

    def get_type(self):
        return "PICKUP"


class IOrderFactory(ABC):
    @abstractmethod
    def create_order(self, order_type: str, *args):
        pass


class NowOrderFactory(IOrderFactory):
    def create_order(self, order_type: str, *args):
        if order_type == "DELIVERY":
            return DeliveryOrder(*args)
        elif order_type == "PICKUP":
            return PickupOrder(*args)
        else:
            raise ValueError("Invalid order type")


class ScheduledOrderFactory(IOrderFactory):
    def __init__(self, schedule_time: str):
        self.schedule_time = schedule_time

    def create_order(self, order_type: str, *args):
        print(f"Order scheduled for {self.schedule_time}")
        if order_type == "DELIVERY":
            return DeliveryOrder(*args)
        elif order_type == "PICKUP":
            return PickupOrder(*args)
        else:
            raise ValueError("Invalid order type")


class NotificationService:
    def notify_user(self, order: Order):
        print(f"Notification sent to {order.user.name} for order {order.order_id}")


class Tomato:
    def __init__(self):
        self.restaurant_manager = RestaurantManager.get_instance()
        self.order_manager = OrderManager.get_instance()
        self.notification_service = NotificationService()

    def place_order(self, order: Order):
        order.pay()
        self.order_manager.add_order(order)
        self.notification_service.notify_user(order)


if __name__ == "__main__":
    tomato = Tomato()

    restaurant = Restaurant(1, "Dominos", "Bangalore")
    pizza = MenuItem("PZ01", "Margherita", 299)
    burger = MenuItem("BG01", "Burger", 149)
    restaurant.add_menu_item(pizza)
    restaurant.add_menu_item(burger)

    tomato.restaurant_manager.add_restaurant(restaurant)

    user = User(101, "Chintan", "Whitefield")
    user.cart.add_to_cart(pizza)
    user.cart.add_to_cart(burger)

    factory = NowOrderFactory()
    order = factory.create_order(
        "DELIVERY",
        1001,
        user,
        restaurant,
        user.cart.items,
        user.address
    )

    order.set_payment_strategy(UPIPayment())
    tomato.place_order(order)
