import pandas as pd
import numpy as np
import json

class Order:

# Here we build basic functions to translate Orders from Json to Python and viceversa.
# The structure of an order is: {"Amount", "Price", "ID", "Side"}

    def Jsontopy(x):
        values = pd.DataFrame(json.loads(x))
        values.columns = ["Amount", "Price", "ID", "Side"]
        return values
    
    def Pytojson(x):
        values = json.dumps(x)
        return values
        
        
class Trade:

# Here we build basic functions to translate Trade Types from Json to Python and viceversa.
# The structure of an order is: {"TakeOrderID", "MarketOrderID", "Amount", "Price"}

    def Jsontopy(x):
        values = pd.DataFrame(json.loads(x))
        values.columns = ["Amount", "Price", "ID", "Side"]
        return values
    
    def Pytojson(x):
        values = json.dumps(x)
        return values
        
        
class OrderBook:
    
# We build in this class the basic functions to add Buy and Sell orders.

# We sort the Buy orders in descending order from lower to higher price
    
    def BuyOrder(buyOrder, OrderBook):
        n = len(OrderBook)
        for i in range(n):
            if buyOrder.Price < OrderBook.Price[i]:
                OrderBook = pd.concat([OrderBook.loc[0:i-1], buyOrder, OrderBook.loc[i:]], axis=0, ignore_index=True)
                break
            elif i == n:
                OrderBook = pd.concat([OrderBook.loc[0:], buyOrder], axis=0, ignore_index=True)
        return OrderBook
                
# We sort the Sell orders in descending order from lower to higher price
                
    def SellOrder(sellOrder, OrderBook):
        n = len(OrderBook)
        for i in range(n):
            if sellOrder.Price < OrderBook.Price[i]:
                OrderBook = pd.concat([OrderBook.loc[0:i-1], buyOrder, OrderBook.loc[i:]], axis=0, ignore_index=True)
                break
            elif i == n:
                OrderBook = pd.concat([OrderBook.loc[0:], buyOrder], axis=0, ignore_index=True)
        return OrderBook

# Next, we build a simple function to remove a buy order from the Order book at a given index

    def RemoveBuyOrder(self, BuyOrder, i):
        del BuyOrder[i]
        return BuyOrder
    
# We do the same to remove a sell order from the Order book at a given index

    def RemoveSellOrder(self, SellOrder, i):
        del SellOrder[i]
        return SellOrder
            

print("##############Testing:")

orderBook = OrderBook()

orderBook.BuyOrder(Order(100,23.7,"order1",0,1))
orderBook.BuyOrder(Order(50,28.4,"order2",0,1))
orderBook.BuyOrder(Order(100,25.9,"order3",0,1))

orderBook.SellOrder(Order(80,25.1,"order1",1,1))
orderBook.SellOrder(Order(40,29.2,"order2",1,1))
orderBook.SellOrder(Order(70,26.3,"order3",1,1))

print("BuyOrders:" + str(len(orderBook.BuyOrders)))
for o in orderBook.BuyOrders:
    o.printOrder()

print("SellOrders:" + str(len(orderBook.SellOrders)))
for o in orderBook.SellOrders:
    o.printOrder()

print("##############Testing Ends")

#orderBook.BuyOrders[1].Amount


#orderBook.RemoveBuyOrder(orderBook.BuyOrders, 0)

#print("BuyOrders:" + str(len(orderBook.BuyOrders)))
#for o in orderBook.BuyOrders:
#    o.printOrder()

# The first part of the code consisted in biulding the OrderBook. The second part of the code will be
# devoted to the matching algorithm.
# We will consider 3 types of orders: market orders, limit orders and cancel orders.

class ProcessOrder:
    
# Considering that the buy (sell) orderbook is ordered in ascending (descending) order, we build the matching algorithm
# with the "FIFO" criteria. According to the FIFO algorithm, buy (sell) orders take priority in the order of price and time. 
# Thus, buy (sell) orders with the same maximum price are prioritized based on the time of bid, and priority is given to 
# the first buy (sell) order. 

# Buy (Sell) Market orders are processed at the best available ask(bid) price.

    def ProcessBuyOrder(self, BuyOrder, SellOrders, m):
# We will build functions to process limit orders and market orders. We will consider both the possibility of a 
# fill of the entire order and a partial fill.
        if BuyOrder.Type == 1:
            n = len(SellOrders)
            index = n - 1
            for o in reversed(range(n)):
                if SellOrders[o].Price < BuyOrder.Price:
                    break
                index = index - 1
            if SellOrders[index].Amount == BuyOrder.Amount:
                orderBook.RemoveSellOrder(orderBook.SellOrders, index)
            elif SellOrders[index].Amount > BuyOrder.Amount: 
                orderBook.SellOrders[index].Amount = orderBook.SellOrders[index].Amount - BuyOrder.Amount
            else:
                BuyOrder.Amount = BuyOrder.Amount - orderBook.SellOrders[index].Amount
                orderBook.RemoveSellOrder(orderBook.SellOrders, index)
                j = index
                while BuyOrder.Amount > 0:
                    for o in reversed(range(j)):
                        if SellOrders[o].Price < BuyOrder.Price:
                            break
                        index = index - 1
                    if SellOrders[index].Amount == BuyOrder.Amount:
                        orderBook.RemoveSellOrder(orderBook.SellOrders, index)
                        BuyOrder.Amount = 0
                    elif SellOrders[index].Amount > BuyOrder.Amount: 
                        orderBook.SellOrders[index].Amount = orderBook.SellOrders[index].Amount - BuyOrder.Amount 
                        BuyOrder.Amount = 0
                    else:
                        BuyOrder.Amount = BuyOrder.Amount - orderBook.SellOrders[index].Amount
                        orderBook.RemoveSellOrder(orderBook.SellOrders, index)
            orderBook.RemoveBuyOrder(orderBook.BuyOrders, m)
        elif BuyOrder.Type == 0:
            while BuyOrder.Amount > 0:
                for i in reversed(range(len(SellOrders))):
                    if SellOrders[i].Amount == BuyOrder.Amount:
                        orderBook.RemoveSellOrder(orderBook.SellOrders, i)
                        BuyOrder.Amount = 0
                    elif SellOrders[index].Amount > BuyOrder.Amount: 
                        orderBook.SellOrders[i].Amount = orderBook.SellOrders[i].Amount - BuyOrder.Amount 
                        BuyOrder.Amount = 0
                    else:
                        BuyOrder.Amount = BuyOrder.Amount - orderBook.SellOrders[i].Amount
                        orderBook.RemoveSellOrder(orderBook.SellOrders, i) 
            orderBook.RemoveBuyOrder(orderBook.BuyOrders, m)
            
            
    def ProcessSellOrder(self, SellOrder, BuyOrders, m):
# We will build functions to process limit orders and market orders. We will consider both the possibility of a 
# fill of the entire order and a partial fill.
        if SellOrder.Type == 1:
            n = len(BuyOrders)
            index = n-1
            for o in reversed(range(n)):
                if BuyOrders[o].Price > SellOrder.Price:
                    break
                index = index - 1 
            if BuyOrders[index].Amount == SellOrder.Amount:
                orderBook.RemoveBuyOrder(orderBook.BuyOrders, index)
            elif BuyOrders[index].Amount > SellOrder.Amount: 
                orderBook.BuyOrders[index].Amount = orderBook.BuyOrders[index].Amount - SellOrder.Amount
            else:
                SellOrder.Amount = SellOrder.Amount - orderBook.BuyOrders[index].Amount
                orderBook.RemoveBuyOrder(orderBook.BuyOrders, index)
                j = index
                while SellOrder.Amount > 0:
                    for o in reversed(range(j)):
                        if BuyOrders[o].Price > SellOrder.Price:
                            break
                        index = index - 1
                    if BuyOrders[index].Amount == SellOrder.Amount:
                        orderBook.RemoveBuyOrder(orderBook.BuyOrders, index)
                        SellOrder.Amount = 0
                    elif BuyOrders[index].Amount > SellOrder.Amount: 
                        orderBook.BuyOrders[index].Amount = orderBook.BuyOrders[index].Amount - SellOrder.Amount 
                        SellOrder.Amount = 0
                    else:
                        SellOrder.Amount = SellOrder.Amount - orderBook.BuyOrders[index].Amount
                        orderBook.RemoveBuyOrder(orderBook.BuyOrders, index)
            orderBook.RemoveSellOrder(orderBook.SellOrders, m)
        elif SellOrder.Type == 0:
            while SellOrder.Amount > 0:
                for i in reversed(range(len(BuyOrders))):
                    if BuyOrders[i].Amount == SellOrder.Amount:
                        orderBook.RemoveBuyOrder(orderBook.BuyOrders, i)
                        SellOrder.Amount = 0
                    elif BuyOrders[index].Amount > SellOrder.Amount: 
                        orderBook.BuyOrders[i].Amount = orderBook.BuyOrders[i].Amount - SellOrder.Amount 
                        SellOrder.Amount = 0
                    else:
                        SellOrder.Amount = SellOrder.Amount - orderBook.BuyOrders[i].Amount
                        orderBook.RemoveBuyOrder(orderBook.BuyOrders, i) 
            orderBook.RemoveSellOrder(orderBook.SellOrders, m)

Process = ProcessOrder()  

m = len(orderBook.SellOrders) - 1

Process.ProcessSellOrder(orderBook.SellOrders[m], orderBook.BuyOrders, m)
            
print("BuyOrders:" + str(len(orderBook.BuyOrders)))
for o in orderBook.BuyOrders:
    o.printOrder()

print("SellOrders:" + str(len(orderBook.SellOrders)))
for o in orderBook.SellOrders:
    o.printOrder()
