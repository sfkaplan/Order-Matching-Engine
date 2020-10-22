import pandas as pd
import numpy as np
import json

class Order:
    Amount = 0
    Price = 0
    ID = ""
    Side = 0
    Type = 0
    
# For Side: 0 = Buy Order, 1 = Sell Order
# For Type: 0 = Market Order, 1 = Limit Order, 2 = Cancel Order

    def __init__(self, amount, price, id, side, type):
        self.Amount = amount
        self.Price = price
        self.ID = id
        self.Side = side
        self.Type = type

    def printOrder(self):
        print("Price:"  + str(self.Price) + " Amount: " + str(self.Amount) + " ID: " + str(self.ID) )
        
class Trade:
    Amount = 0
    Price = 0
    ID = ""
    Side = 0
    
# We build in this class the basic functions to add Buy and Sell orders.

# We sort the Buy (sell) orders in ascending (descending) order from lower (higher) to higher (lower) price
        
        
class OrderBook:

    BuyOrders = []
    SellOrders = []

    def BuyOrder(self, newOrder):
        index = 0
        if newOrder.Type == 0:
            self.BuyOrders.insert(index, newOrder)
        else:
            for o in self.BuyOrders:
                if o.Price > newOrder.Price:
                    break
                index += 1
            self.BuyOrders.insert(index, newOrder)

    def SellOrder(self, newOrder):
        if newOrder.Type == 0:
            index = len(newOrder)
            self.SellOrders.insert(index, newOrder)
        else:
            index = 0
            for o in self.SellOrders:
                if o.Price < newOrder.Price:
                    break
                index += 1
            self.SellOrders.insert(index, newOrder)
        
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
