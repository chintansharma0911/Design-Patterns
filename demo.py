# Factory Method ####################################
#####################################################
# from factory.FrenchLocaliserFactory import FrenchLocaliserFactory
# from factory.EnglishLocaliserFactory import EnglishLocaliserFactory
#
#
# if __name__ == "__main__":
#     frenchlocaliser = FrenchLocaliserFactory().createLocaliser()
#     englishlocaliser = EnglishLocaliserFactory().createLocaliser()
#
#     message = ["car", "bike", "cycle"]
#
#     for msg in message:
#         print(frenchlocaliser.localise(msg))
#         print(englishlocaliser.localise(msg))

# Adapter Method
# from adapter.SquareAdapter import RoundCicle, SquareAdapter, SquarePeg
# circle =RoundCicle(2)
# square = SquarePeg(4)
#
# print(circle.get_radius())
# print(SquareAdapter(square).get_radius())


# Bridge
# from bridge.fileStorage import AdvanceFileStorage, CloudStorage, Networktorage
#
# cloud = CloudStorage()
# network = Networktorage()
# advanceStorage1 = AdvanceFileStorage(cloud)
# advanceStorage2 = AdvanceFileStorage(network)
# advanceStorage1.saveFile()
# advanceStorage2.saveFile()


# Composite Calculator
# from composite.calculator import Number, Expression
# print(Expression(Number(7),Expression(Number(3),Number(4),'+'), '*').evaluate())
#
# from composite.fileStorage import File, Directory
# if __name__ == "__main__":
#     # Create files
#     file1 = File("resume.pdf", 120)
#     file2 = File("photo.jpg", 450)
#     file3 = File("song.mp3", 5000)
#     file4 = File("notes.txt", 30)
#
#     # Create directories
#     documents = Directory("Documents")
#     pictures = Directory("Pictures")
#     music = Directory("Music")
#     root = Directory("Root")
#
#     # Build tree
#     documents.add(file1)
#     documents.add(file4)
#
#     pictures.add(file2)
#     music.add(file3)
#
#     root.add(documents)
#     root.add(pictures)
#     root.add(music)
#     root.add(File('Chintan', 100))
#
#     # Show structure
#     print("📂 File System Structure:")
#     root.showDetails()
#
#     # Show total size
#     print("\n📊 Total Size:", root.getSize(), "KB")


# Decorator Method  ----> Pizza toppings, Coffee Order
# from decorator.coffeeOrder import Caramel, Decaf, WhippedMilk, Espresso
# order = Espresso()
# print(order.get_desc())
# print(order.get_cost())
#
# order = WhippedMilk(order)
# print(order.get_desc())
# print(order.get_cost())
#
# order = Caramel(order)
# print(order.get_desc())
# print(order.get_cost())


# Proxy Design
# from proxy.cacheDatabase import RealDatabaseQuery, CacheProxy
# import time
# # Client code
# if __name__ == "__main__":
#     # Create the Real Subject
#     real_database_query = RealDatabaseQuery()
#
#     # Create the Cache Proxy with a cache duration of 5 seconds
#     cache_proxy = CacheProxy(real_database_query, cache_duration_seconds=5)
#
#     # Perform database queries, some of which will be cached
#     print(cache_proxy.execute_query("SELECT * FROM table1"))
#     print(cache_proxy.execute_query("SELECT * FROM table2"))
#     time.sleep(3)  # Sleep for 3 seconds
#
#     # Should return cached result
#     print(cache_proxy.execute_query("SELECT * FROM table1"))
#
#     print(cache_proxy.execute_query("SELECT * FROM table3"))

# Client code
# from proxy.performaceMonitor import MonitoringProxy
# if __name__ == "__main__":
#     # Create the Monitoring Proxy (lazy loading of Real Subject)
#     monitoring_proxy = MonitoringProxy()
#
#     # Client interacts with the Proxy
#     monitoring_proxy.perform_operation()


# Chain of responsibbility
# from chainOfResponsibility.Middleware import LoggingMiddleware, DataValidationMiddleware, AuthenticationMiddleware
#
#
# class Chain:
#     def __init__(self):
#         self.middlewares = []
#
#     def add_middleware(self, middleware):
#         self.middlewares.append(middleware)
#
#     def handle_request(self, request):
#         for middleware in self.middlewares:
#             request = middleware.handle_request(request)
#             if request is None:
#                 print("Request processing stopped.")
#                 break
#
# # Client code to create and configure the middleware chain.
# if __name__ == "__main__":
#     # Create middleware instances.
#     auth_middleware = AuthenticationMiddleware()
#     logging_middleware = LoggingMiddleware()
#     data_validation_middleware = DataValidationMiddleware()
#
#     # Create the chain and add middleware.
#     chain = Chain()
#     chain.add_middleware(auth_middleware)
#     chain.add_middleware(logging_middleware)
#     chain.add_middleware(data_validation_middleware)
#
#     # Simulate an HTTP request.
#     http_request = {"user": "username", "data": "valid_data"}
# #     chain.handle_request(http_request)
# from chainOfResponsibility.logger import Request, AuthenticationHandler, DataValidationHandler, LoggingHandler
#
# if __name__ == "__main__":
#     request = Request({"token": "abc123", "data": "some_data"})
#
#     logging_handler = LoggingHandler(DataValidationHandler(AuthenticationHandler()))
#
#     logging_handler.handle_request(request)
#
#     if request.valid:
#         print("Request processing successful")
#     else:
#         print("Request processing failed")


# Command Pattern
# # ------------------- Client Code -------------------
# from command.RemoteControl import LightBulb, AirConditioner, LightOnCommand, LightOffCommand, ACOnCommand, ACOffCommand, \
#     RemoteControl
#
# if __name__ == "__main__":
#     # Receivers
#     light = LightBulb()
#     ac = AirConditioner()
#
#     # Commands
#     light_on = LightOnCommand(light)
#     light_off = LightOffCommand(light)
#     ac_on = ACOnCommand(ac)
#     ac_off = ACOffCommand(ac)
#
#     # Invoker
#     remote = RemoteControl()
#
#     # Use case
#     remote.execute_command(light_on)   # 💡 Light is ON
#     remote.execute_command(ac_on)      # ❄️ AC is ON
#     remote.undo()                      # ❄️ AC is OFF
#     remote.undo()                      # 💡 Light is OFF
#     remote.redo()                      # 💡 Light is ON
#     remote.execute_command(ac_off)     # ❄️ AC is OFF
#     remote.redo()                      # Nothing to redo


#
# # Mediator ---------> Chat function, Auction
# from mediator.auction import Bidder, AuctionMediator
# iplAuction = AuctionMediator('ipl')
# fplAuction = AuctionMediator('fpl')
#
# rahul = Bidder('Rahul')
# aman = Bidder('aman')
# piyush = Bidder('piyush')
# kishan = Bidder('kishan')
# karun = Bidder('karun')
#
# iplAuction.addBidder(karun)
# iplAuction.addBidder(piyush)
# iplAuction.addBidder(aman)
#
#
# fplAuction.addBidder(rahul)
# fplAuction.addBidder(piyush)
# fplAuction.addBidder(karun)
# fplAuction.addBidder(kishan)
#
#
#
#
# rahul.bid(100,fplAuction)
# print('=================')
# aman.bid(200, fplAuction)
# print('=================')
# piyush.bid(500, fplAuction)
# print('=================')
# karun.bid(800, iplAuction)
# print('=================')

# Observer Pattern
# from observer.pubsub import ChatRoom,ChatMember
# # # Step [4]: Client
# if __name__ == "__main__":
#     # Create a chat room
#     general_chat = ChatRoom()
#
#     # Create participants
#     user1 = ChatMember("User1")
#     user2 = ChatMember("User2")
#     user3 = ChatMember("User3")
#
#     # Participants join the chat room
#     general_chat.join(user1)
#     general_chat.join(user2)
#     general_chat.join(user3)
#
#     # Send a message to the chat room
#     general_chat.broadcast("Hi!")



# State Design Pattern
# from state.IdleState import IdleState
# from state.DispensingState import DispensingState
# from state.SelectProductState import SelectProductState
# from state.HasMoneyState import HasMoneyState
# from state.vendingMachine import Machine
#
# vendingMachine = Machine()
# vendingMachine.setInventory(
#     {'101': {'price': 100},
#      '102': {'price': 300},
#      '103': {'price': 200}
#      }
# )
#
#
# currentState = vendingMachine.getState()
# currentState.clickOnInsertCoinButton(vendingMachine)
#
#
# currentState = vendingMachine.getState()
# currentState.insertCoin(vendingMachine, [50,60,122])
#
# currentState.clickOnStartProductSelection(vendingMachine)
#
# currentState = vendingMachine.getState()
# currentState.chooseProduct(vendingMachine, '101')
#
#
# currentState = vendingMachine.getState()
# currentState.dispenseProduct(vendingMachine, '101')
#
# print(vendingMachine.getInventory())
# print(vendingMachine.getState())





# # StrategyPattern
# from strategy.trading import TradingContext, MovingAverageStrategy, MeanReversionStrategy
#
# if __name__ == "__main__":
#     # Sample data for trading
#     trading_data = [50, 55, 45, 60, 50]
#
#     # Create concrete strategy objects
#     moving_average_strategy = MovingAverageStrategy()
#     mean_reversion_strategy = MeanReversionStrategy()
#
#     # Create context with a default strategy
#     trading_context = TradingContext(moving_average_strategy)
#
#     # Execute the default strategy
#     result = trading_context.execute_trade(trading_data)
#     print(result)  # Output: Executing Moving Average Trading Strategy. Moving Average: 51.67
#
#     # Switch to a different strategy at runtime
#     trading_context.set_strategy(mean_reversion_strategy)
#
#     # Execute the updated strategy
#     result = trading_context.execute_trade(trading_data)
#     print(result)  # Output: Executing Mean Reversion Trading Strategy. Deviation from Mean: -1.00
