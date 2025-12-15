from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
import math
import itertools

# ==========================
# Models
# ==========================

class Product:
    def __init__(self, sku: int, name: str, price: float):
        self.sku = sku
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product(sku={self.sku}, name={self.name}, price={self.price})"


class User:
    def __init__(self, name: str, x: float, y: float):
        self.name = name
        self.x = x
        self.y = y
        self.cart = Cart()

    def __repr__(self):
        return f"User({self.name})"


class DeliveryPartner:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"DeliveryPartner({self.name})"


class Order:
    _id_gen = itertools.count(1)

    def __init__(self, user: User, items: List[Tuple[int, int]],
                 partners: List[DeliveryPartner], total: float):
        self.order_id = next(Order._id_gen)
        self.user = user
        self.items = items
        self.partners = partners
        self.total = total

    def __repr__(self):
        return f"Order(id={self.order_id}, user={self.user.name}, total={self.total})"


# ==========================
# Cart
# ==========================

class Cart:
    def __init__(self):
        self.items: Dict[int, int] = {}  # sku -> qty

    def add_item(self, sku: int, qty: int):
        self.items[sku] = self.items.get(sku, 0) + qty

    def get_items(self) -> Dict[int, int]:
        return self.items

    def clear(self):
        self.items.clear()


# ==========================
# Product Factory
# ==========================

class ProductFactory:
    @staticmethod
    def create_product(sku: int, name: str, price: float) -> Product:
        return Product(sku, name, price)


# ==========================
# Inventory Store (Abstract)
# ==========================

class InventoryStore(ABC):

    @abstractmethod
    def add_product(self, product: Product, qty: int):
        pass

    @abstractmethod
    def remove_product(self, sku: int, qty: int):
        pass

    @abstractmethod
    def check_stock(self, sku: int) -> int:
        pass

    @abstractmethod
    def list_all_products(self) -> Dict[int, Product]:
        pass


# ==========================
# DB Inventory Store
# ==========================

class DBInventoryStore(InventoryStore):
    def __init__(self):
        self.stock: Dict[int, int] = {}
        self.products: Dict[int, Product] = {}

    def add_product(self, product: Product, qty: int):
        self.products[product.sku] = product
        self.stock[product.sku] = self.stock.get(product.sku, 0) + qty

    def remove_product(self, sku: int, qty: int):
        if self.stock.get(sku, 0) < qty:
            raise Exception("Insufficient stock")
        self.stock[sku] -= qty

    def check_stock(self, sku: int) -> int:
        return self.stock.get(sku, 0)

    def list_all_products(self) -> Dict[int, Product]:
        return self.products


# ==========================
# Inventory Manager
# ==========================

class InventoryManager:
    def __init__(self, store: InventoryStore):
        self.store = store

    def add_stock(self, sku: int, qty: int):
        product = self.store.products.get(sku)
        if not product:
            raise Exception("Product not found")
        self.store.add_product(product, qty)

    def remove_stock(self, sku: int, qty: int):
        self.store.remove_product(sku, qty)

    def check_stock(self, sku: int) -> int:
        return self.store.check_stock(sku)

    def get_available_products(self) -> Dict[int, Product]:
        return self.store.list_all_products()


# ==========================
# Replenish Strategy (Abstract)
# ==========================

class ReplenishStrategy(ABC):

    @abstractmethod
    def replenish(self, inventory_mgr: InventoryManager,
                  items: Dict[int, int]):
        pass


class ThresholdReplenishStrategy(ReplenishStrategy):
    def __init__(self, threshold: int):
        self.threshold = threshold

    def replenish(self, inventory_mgr: InventoryManager,
                  items: Dict[int, int]):
        for sku, qty in items.items():
            if inventory_mgr.check_stock(sku) < self.threshold:
                inventory_mgr.add_stock(sku, qty)


class WeeklyReplenishStrategy(ReplenishStrategy):
    def replenish(self, inventory_mgr: InventoryManager,
                  items: Dict[int, int]):
        for sku, qty in items.items():
            inventory_mgr.add_stock(sku, qty)


# ==========================
# Dark Store
# ==========================

class DarkStore:
    def __init__(self, name: str, x: float, y: float,
                 inventory_mgr: InventoryManager,
                 replenish_strategy: ReplenishStrategy):
        self.name = name
        self.x = x
        self.y = y
        self.inventory_mgr = inventory_mgr
        self.replenish_strategy = replenish_strategy

    def distance_to(self, x: float, y: float) -> float:
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def get_all_products(self) -> Dict[int, Product]:
        return self.inventory_mgr.get_available_products()

    def run_replenish(self, items: Dict[int, int]):
        self.replenish_strategy.replenish(self.inventory_mgr, items)

    def __repr__(self):
        return f"DarkStore({self.name})"


# ==========================
# Dark Store Manager (Singleton)
# ==========================

class DarkStoreManager:
    _instance = None

    def __init__(self):
        self.stores: List[DarkStore] = []

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = DarkStoreManager()
        return cls._instance

    def add_store(self, store: DarkStore):
        self.stores.append(store)

    def get_nearby_stores(self, x: float, y: float, max_dist: float) -> List[DarkStore]:
        return [s for s in self.stores if s.distance_to(x, y) <= max_dist]


# ==========================
# Order Manager (Singleton)
# ==========================

class OrderManager:
    _instance = None

    def __init__(self):
        self.orders: List[Order] = []

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = OrderManager()
        return cls._instance

    def place_order(self, user: User, cart: Cart,
                    darkstore_mgr: DarkStoreManager) -> Order:

        stores = darkstore_mgr.get_nearby_stores(user.x, user.y, max_dist=10)
        if not stores:
            raise Exception("No nearby stores")

        store = stores[0]
        total = 0.0

        for sku, qty in cart.get_items().items():
            if store.inventory_mgr.check_stock(sku) < qty:
                raise Exception("Stock unavailable")
            product = store.inventory_mgr.store.products[sku]
            total += product.price * qty
            store.inventory_mgr.remove_stock(sku, qty)

        partners = [DeliveryPartner("AutoAssigned")]
        order = Order(user, list(cart.get_items().items()), partners, total)
        self.orders.append(order)
        cart.clear()
        return order


# ==========================
# Zepto Orchestrator
# ==========================

class Zepto:
    def __init__(self):
        self.darkstore_mgr = DarkStoreManager.instance()
        self.order_mgr = OrderManager.instance()

    def register_darkstore(self, store: DarkStore):
        self.darkstore_mgr.add_store(store)

    def place_order(self, user: User) -> Order:
        return self.order_mgr.place_order(user, user.cart, self.darkstore_mgr)


# ==========================
# Example Usage
# ==========================

if __name__ == "__main__":
    # Create products
    p1 = ProductFactory.create_product(1, "Milk", 50)
    p2 = ProductFactory.create_product(2, "Bread", 30)

    # Inventory setup
    store_db = DBInventoryStore()
    store_db.add_product(p1, 100)
    store_db.add_product(p2, 50)

    inventory_mgr = InventoryManager(store_db)
    replenish_strategy = ThresholdReplenishStrategy(threshold=10)

    dark_store = DarkStore("DS-1", 0, 0, inventory_mgr, replenish_strategy)

    # Zepto
    zepto = Zepto()
    zepto.register_darkstore(dark_store)

    # User flow
    user = User("Chintan", 1, 1)
    user.cart.add_item(1, 2)
    user.cart.add_item(2, 1)

    order = zepto.place_order(user)
    print(order)
