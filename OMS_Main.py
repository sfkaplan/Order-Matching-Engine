import pandas as pd
import numpy as np
import copy

class Order:
    Amount = 0
    Price = 0
    ID = ""
    SIDE_BUY = 0
    SIDE_SELL = 1
    TYPE_MARKETORDER = 0
    TYPE_LIMITORDER = 1
    TYPE_CANCELORDER = 2
    
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

class TransactionBook:

    def BuyTransaction(self, newTransaction, transactionBook):
        index = len(transactionBook)
        transactionBook.append(newTransaction)

    def SellTransaction(self, newTransaction, transactionBook):
        index = len(transactionBook)
        transactionBook.append(newTransaction)
            

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

Transactions = TransactionBook()
transactionBook = []

#orderBook.BuyOrders[1].Amount


#orderBook.RemoveBuyOrder(orderBook.BuyOrders, 0)

#print("BuyOrders:" + str(len(orderBook.BuyOrders)))
#for o in orderBook.BuyOrders:
#    o.printOrder()

# The first part of the code consisted in building the OrderBook. The second part of the code will be
# devoted to the matching algorithm.
# We will consider 3 types of orders: market orders, limit orders and cancel orders.

class ProcessOrderAllocation:
    
# We will apply the Allocation algorithm to the matching process.
# Basic idea of this algorithm: it prioritizes the first incoming order that betters the market.
# Afterwards, it applies a pro-rata algorithm to allocate the amount that wasn't filled by the first order with 
# a minimum of two lots.
# Since all fills are rounded down to the nearest integer, any excess lots are allocated using FIFO. 

# Buy (Sell) Market orders are processed at the best available ask(bid) price.

    def ProcessBuyOrder(self, BuyOrder, SellOrders, m):
# We will build functions to process limit orders and market orders. We will consider both the possibility of a 
# fill of the entire order and a partial fill.
        if BuyOrder.Type == 1:
            n = len(SellOrders)
            index = n-1
            for o in reversed(range(n)):
                if SellOrders[o].Price < BuyOrder.Price:
                    break
                else:
                    index = index - 1
            print(index)
            if SellOrders[index].Price > BuyOrder.Price:
                print("No Order has been processed")
            else:
                alloc = []
                alloc.append(SellOrders[index])
                for o in reversed(range(index)):
                    if SellOrders[o].Price == BuyOrder.Price:
                        alloc.append(SellOrders[o])
                    else:
                        break
                if len(alloc) == 1:
                    if SellOrders[index].Amount == BuyOrder.Amount:
                        Transactions.SellTransaction(SellOrders[index], transactionBook)
                        Transactions.BuyTransaction(BuyOrder, transactionBook)
                        orderBook.RemoveSellOrder(orderBook.SellOrders, index)
                        orderBook.RemoveBuyOrder(orderBook.BuyOrders, m)
                    elif SellOrders[index].Amount > BuyOrder.Amount: 
                        SellTransaction = copy.deepcopy(orderBook.SellOrders[index])
                        SellTransaction.Amount = BuyOrder.Amount
                        Transactions.SellTransaction(SellTransaction, transactionBook)
                        Transactions.BuyTransaction(BuyOrder, transactionBook)
                        orderBook.SellOrders[index].Amount = orderBook.SellOrders[index].Amount - BuyOrder.Amount 
                        orderBook.RemoveBuyOrder(orderBook.BuyOrders, m)
                    else:
                        BuyTransaction = copy.deepcopy(BuyOrder)
                        BuyTransaction.Amount = SellOrders[index].Amount
                        BuyTransaction.Price = SellOrders[index].Price
                        Transactions.SellTransaction(orderBook.SellOrders[index], transactionBook)
                        Transactions.BuyTransaction(BuyTransaction, transactionBook)
                        BuyOrder.Amount = BuyOrder.Amount - orderBook.SellOrders[index].Amount
                        orderBook.RemoveSellOrder(orderBook.SellOrders, index)
                        index = index - 1
                        while BuyOrder.Amount > 0:
                            for o in reversed(range(index+1)):
                                if SellOrders[o].Price < BuyOrder.Price:
                                    break
                                else:
                                    index = index - 1
                            if SellOrders[index].Price > BuyOrder.Price:
                                break
                            else:
                                if SellOrders[index].Amount == BuyOrder.Amount:
                                    Transactions.SellTransaction(Sellorders[index], transactionBook)
                                    Transactions.BuyTransaction(BuyOrder, transactionBook)
                                    orderBook.RemoveSellOrder(orderBook.SellOrders, index)
                                    BuyOrder.Amount = 0
                                elif SellOrders[index].Amount > BuyOrder.Amount: 
                                    SellTransaction = copy.deepcopy(orderBook.SellOrders[index])
                                    SellTransaction.Amount = BuyOrder.Amount
                                    BuyTransaction = copy.deepcopy(BuyOrder)
                                    Transactions.SellTransaction(SellTransaction, transactionBook)
                                    Transactions.BuyTransaction(BuyTransaction, transactionBook)
                                    orderBook.SellOrders[index].Amount = orderBook.SellOrders[index].Amount - BuyOrder.Amount
                                    BuyOrder.Amount = 0
                                else:
                                    BuyTransaction = copy.deepcopy(BuyOrder)
                                    BuyTransaction.Amount = SellOrders[index].Amount
                                    BuyTransaction.Price = SellOrders[index].Price
                                    Transactions.SellTransaction(orderBook.SellOrders[index], transactionBook)
                                    Transactions.BuyTransaction(BuyTransaction, transactionBook)
                                    BuyOrder.Amount = BuyOrder.Amount - orderBook.SellOrders[index].Amount
                                    orderBook.RemoveSellOrder(orderBook.SellOrders, index)
                                    index = index - 1
                else:
                    if SellOrders[index].Amount == BuyOrder.Amount:
                        Transactions.SellTransaction(SellOrders[index], transactionBook)
                        Transactions.BuyTransaction(BuyOrder, transactionBook)
                        orderBook.RemoveSellOrder(orderBook.SellOrders, index)
                        orderBook.RemoveBuyOrder(orderBook.BuyOrders, m) 
                    elif SellOrders[index].Amount > BuyOrder.Amount: 
                        SellTransaction = copy.deepcopy(orderBook.SellOrders[index])
                        SellTransaction.Amount = BuyOrder.Amount
                        Transactions.SellTransaction(SellTransaction, transactionBook)
                        Transactions.BuyTransaction(BuyOrder, transactionBook)
                        orderBook.SellOrders[index].Amount = orderBook.SellOrders[index].Amount - BuyOrder.Amount 
                        orderBook.RemoveBuyOrder(orderBook.BuyOrders, m)
                    else:
                        BuyTransaction = copy.deepcopy(BuyOrder)
                        BuyTransaction.Amount = SellOrders[index].Amount
                        BuyTransaction.Price = SellOrders[index].Price
                        Transactions.SellTransaction(orderBook.SellOrders[index], transactionBook)
                        Transactions.BuyTransaction(BuyTransaction, transactionBook)
                        BuyOrder.Amount = BuyOrder.Amount - orderBook.SellOrders[index].Amount
                        orderBook.RemoveSellOrder(orderBook.SellOrders, index)
                        pro_rata_rates = []
                        pro_rata_sum = []
                        pro_rata_amounts = []
                        for i in range(1,len(alloc)):
                            pro_rata_sum.append(alloc[i].Amount)
                        pro_rata_sum = sum(pro_rata_sum)
                        for i in range(1,len(alloc)):
                            pro_rata_rates.append(alloc[i].Amount/pro_rata_sum)
                        for i in range(len(alloc)-1):
                            pro_rata_amounts.append(int(pro_rata_rates[i]*BuyOrder.Amount))
                        BuyTransaction2 = copy.deepcopy(BuyOrder)
                        BuyTransaction2.Amount = BuyOrder.Amount
                        BuyTransaction2.Price = SellOrders[index+1].Price
                        for i in range(1,len(alloc)):
                            SellTransactionaux = copy.deepcopy(orderBook.SellOrders[index+i])
                            SellTransactionaux.Amount = pro_rata_amounts[i-1]
                            SellTransactionMat.append(SellTransactionaux)
                        for i in range(len(alloc)-1):
                            Transactions.SellTransaction(SellTransactionMat[i], transactionBook)
                        for i in range(1,len(alloc)):
                                orderBook.SellOrders[index+i].Amount = orderBook.SellOrders[index+i].Amount - SellTransactionMat[i-1].Amount 
                        if sum(SellTransactionMat) < BuyTransaction2.Amount:
                            SellTransactionaux2 = copy.deepcopy(SellTransactionMat[0])
                            SellTransactionaux2. Amount = BuyTransaction2.Amount - sum(SellTransactionMat)
                            Transactions.SellTransaction(SellTransactionaux2, transactionBook)
                            orderBook.SellOrders[index+1].Amount = orderBook.SellOrders[index+1].Amount - SellTransactionaux2. Amount 
                        Transactions.BuyTransaction(BuyTransaction2, transactionBook)
                        orderBook.RemoveBuyOrder(orderBook.BuyOrders, m)
            if BuyOrder.Amount == 0:
                orderBook.RemoveBuyOrder(orderBook.BuyOrders, m)
        elif BuyOrder.Type == 0:
            while BuyOrder.Amount > 0:
                for i in reversed(range(len(SellOrders))):
                    if SellOrders[i].Amount == BuyOrder.Amount:
                        Transactions.SellTransaction(Sellorders[index], transactionBook)
                        Transactions.BuyTransaction(BuyOrder, transactionBook)
                        orderBook.RemoveSellOrder(orderBook.SellOrders, i)
                        BuyOrder.Amount = 0
                    elif SellOrders[index].Amount > BuyOrder.Amount: 
                        SellTransaction = copy.deepcopy(orderBook.SellOrders[index])
                        SellTransaction.Amount = BuyOrder.Amount
                        BuyTransaction = copy.deepcopy(BuyOrder)
                        Transactions.SellTransaction(SellTransaction, transactionBook)
                        Transactions.BuyTransaction(BuyTransaction, transactionBook)
                        orderBook.SellOrders[i].Amount = orderBook.SellOrders[i].Amount - BuyOrder.Amount 
                        BuyOrder.Amount = 0
                    else:
                        BuyTransaction = copy.deepcopy(BuyOrder)
                        BuyTransaction.Amount = SellOrders[index].Amount
                        BuyTransaction.Price = SellOrders[index].Price
                        Transactions.SellTransaction(orderBook.SellOrders[index], transactionBook)
                        Transactions.BuyTransaction(BuyTransaction, transactionBook)
                        BuyOrder.Amount = BuyOrder.Amount - orderBook.SellOrders[i].Amount
                        orderBook.RemoveSellOrder(orderBook.SellOrders, i) 
            if BuyOrder.Amount == 0:
                orderBook.RemoveBuyOrder(orderBook.BuyOrders, m)
            print("Limit Buy Order " + BuyOrder.ID +  " has been processed")
        else:
            Cancel = CancelOrder()
            Cancel.CancelBuyOrder(BuyOrder, orderBook.BuyOrders, m)
    
    def ProcessSellOrder(self, SellOrder, BuyOrders, m):
# We will build functions to process limit orders and market orders. We will consider both the possibility of a 
# fill of the entire order and a partial fill.
        if SellOrder.Type == 1:
            n = len(BuyOrders)
            index = n-1
            for o in reversed(range(n)):
                if BuyOrders[o].Price > SellOrder.Price:
                    break
                else:
                    index = index - 1 
            print(index)
            if BuyOrders[index].Price < SellOrder.Price:
                print("No Order has been processed")
            else:
                if BuyOrders[index].Amount == SellOrder.Amount:
                    Transactions.BuyTransaction(BuyOrders[index], transactionBook)
                    Transactions.SellTransaction(SellOrder, transactionBook)
                    orderBook.RemoveBuyOrder(orderBook.BuyOrders, index)
                elif BuyOrders[index].Amount > SellOrder.Amount: 
                    BuyTransaction = copy.deepcopy(orderBook.BuyOrders[index])
                    BuyTransaction.Amount = SellOrder.Amount
                    SellTransaction = copy.deepcopy(SellOrder)
                    Transactions.BuyTransaction(BuyTransaction, transactionBook)
                    Transactions.SellTransaction(SellTransaction, transactionBook)
                    orderBook.BuyOrders[index].Amount = orderBook.BuyOrders[index].Amount - SellOrder.Amount
                else:
                    SellTransaction = copy.deepcopy(SellOrder)
                    SellTransaction.Amount = BuyOrders[index].Amount
                    SellTransaction.Price = BuyOrders[index].Price
                    Transactions.BuyTransaction(orderBook.BuyOrders[index], transactionBook)
                    Transactions.SellTransaction(SellTransaction, transactionBook)
                    SellOrder.Amount = SellOrder.Amount - orderBook.BuyOrders[index].Amount
                    orderBook.RemoveBuyOrder(orderBook.BuyOrders, index)
                    index = index - 1
                    while SellOrder.Amount > 0:
                        for o in reversed(range(index+1)):
                            if BuyOrders[o].Price > SellOrder.Price:
                                break
                            else:
                                index = index - 1
                        if BuyOrders[index].Price < SellOrder.Price:
                            break
                        else:
                            if BuyOrders[index].Amount == SellOrder.Amount:
                                Transactions.SellTransaction(SellOrder, transactionBook)
                                Transactions.BuyTransaction(BuyOrders[index], transactionBook)
                                orderBook.RemoveBuyOrder(orderBook.BuyOrders, index)
                                SellOrder.Amount = 0
                            elif BuyOrders[index].Amount > SellOrder.Amount: 
                                BuyTransaction = copy.deepcopy(orderBook.BuyOrders[index])
                                BuyTransaction.Amount = SellOrder.Amount
                                SellTransaction = copy.deepcopy(SellOrder)
                                Transactions.BuyTransaction(BuyTransaction, transactionBook)
                                Transactions.SellTransaction(SellTransaction, transactionBook)
                                orderBook.BuyOrders[index].Amount = orderBook.BuyOrders[index].Amount - SellOrder.Amount 
                                SellOrder.Amount = 0
                            else:
                                SellTransaction = copy.deepcopy(SellOrder)
                                SellTransaction.Amount = BuyOrders[index].Amount
                                SellTransaction.Price = BuyOrders[index].Price
                                Transactions.BuyTransaction(orderBook.BuyOrders[index], transactionBook)
                                Transactions.SellTransaction(SellTransaction, transactionBook)
                                SellOrder.Amount = SellOrder.Amount - orderBook.BuyOrders[index].Amount
                                orderBook.RemoveBuyOrder(orderBook.BuyOrders, index)
                                index = index - 1
            if SellOrder.Amount == 0:
                orderBook.RemoveSellOrder(orderBook.SellOrders, m)
        elif SellOrder.Type == 0:
            while SellOrder.Amount > 0:
                for i in range(len(BuyOrders)):
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
            print("Market Sell Order " + SellOrder.ID +  " has been processed")
        else:
            Cancel = CancelOrder()
            Cancel.CancelSellOrder(SellOrder, orderBook.SellOrders, m)

class ProcessOrderFifo:
    
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
            index = n-1
            for o in reversed(range(n)):
                if SellOrders[o].Price < BuyOrder.Price:
                    break
                else:
                    index = index - 1
            print(index)
            if SellOrders[index].Price > BuyOrder.Price:
                print("No Order has been processed")
            else:
                if SellOrders[index].Amount == BuyOrder.Amount:
                    Transactions.SellTransaction(SellOrders[index], transactionBook)
                    Transactions.BuyTransaction(BuyOrder, transactionBook)
                    orderBook.RemoveSellOrder(orderBook.SellOrders, index)
                elif SellOrders[index].Amount > BuyOrder.Amount: 
                    SellTransaction = copy.deepcopy(orderBook.SellOrders[index])
                    SellTransaction.Amount = BuyOrder.Amount
                    Transactions.SellTransaction(SellTransaction, transactionBook)
                    Transactions.BuyTransaction(BuyOrder, transactionBook)
                    orderBook.SellOrders[index].Amount = orderBook.SellOrders[index].Amount - BuyOrder.Amount    
                else:
                    BuyTransaction = copy.deepcopy(BuyOrder)
                    BuyTransaction.Amount = SellOrders[index].Amount
                    BuyTransaction.Price = SellOrders[index].Price
                    Transactions.SellTransaction(orderBook.SellOrders[index], transactionBook)
                    Transactions.BuyTransaction(BuyTransaction, transactionBook)
                    BuyOrder.Amount = BuyOrder.Amount - orderBook.SellOrders[index].Amount
                    orderBook.RemoveSellOrder(orderBook.SellOrders, index)
                    index = index - 1
                    while BuyOrder.Amount > 0:
                        for o in reversed(range(index+1)):
                            if SellOrders[o].Price < BuyOrder.Price:
                                break
                            else:
                                index = index - 1
                        if SellOrders[index].Price > BuyOrder.Price:
                            break
                        else:
                            if SellOrders[index].Amount == BuyOrder.Amount:
                                Transactions.SellTransaction(Sellorders[index], transactionBook)
                                Transactions.BuyTransaction(BuyOrder, transactionBook)
                                orderBook.RemoveSellOrder(orderBook.SellOrders, index)
                                BuyOrder.Amount = 0
                            elif SellOrders[index].Amount > BuyOrder.Amount: 
                                SellTransaction = copy.deepcopy(orderBook.SellOrders[index])
                                SellTransaction.Amount = BuyOrder.Amount
                                BuyTransaction = copy.deepcopy(BuyOrder)
                                Transactions.SellTransaction(SellTransaction, transactionBook)
                                Transactions.BuyTransaction(BuyTransaction, transactionBook)
                                orderBook.SellOrders[index].Amount = orderBook.SellOrders[index].Amount - BuyOrder.Amount
                                BuyOrder.Amount = 0
                            else:
                                BuyTransaction = copy.deepcopy(BuyOrder)
                                BuyTransaction.Amount = SellOrders[index].Amount
                                BuyTransaction.Price = SellOrders[index].Price
                                Transactions.SellTransaction(orderBook.SellOrders[index], transactionBook)
                                Transactions.BuyTransaction(BuyTransaction, transactionBook)
                                BuyOrder.Amount = BuyOrder.Amount - orderBook.SellOrders[index].Amount
                                orderBook.RemoveSellOrder(orderBook.SellOrders, index)
                                index = index - 1
            if BuyOrder.Amount == 0:
                orderBook.RemoveBuyOrder(orderBook.BuyOrders, m)
        elif BuyOrder.Type == 0:
            while BuyOrder.Amount > 0:
                for i in reversed(range(len(SellOrders))):
                    if SellOrders[i].Amount == BuyOrder.Amount:
                        Transactions.SellTransaction(Sellorders[index], transactionBook)
                        Transactions.BuyTransaction(BuyOrder, transactionBook)
                        orderBook.RemoveSellOrder(orderBook.SellOrders, i)
                        BuyOrder.Amount = 0
                    elif SellOrders[index].Amount > BuyOrder.Amount: 
                        SellTransaction = copy.deepcopy(orderBook.SellOrders[index])
                        SellTransaction.Amount = BuyOrder.Amount
                        BuyTransaction = copy.deepcopy(BuyOrder)
                        Transactions.SellTransaction(SellTransaction, transactionBook)
                        Transactions.BuyTransaction(BuyTransaction, transactionBook)
                        orderBook.SellOrders[i].Amount = orderBook.SellOrders[i].Amount - BuyOrder.Amount 
                        BuyOrder.Amount = 0
                    else:
                        BuyTransaction = copy.deepcopy(BuyOrder)
                        BuyTransaction.Amount = SellOrders[index].Amount
                        BuyTransaction.Price = SellOrders[index].Price
                        Transactions.SellTransaction(orderBook.SellOrders[index], transactionBook)
                        Transactions.BuyTransaction(BuyTransaction, transactionBook)
                        BuyOrder.Amount = BuyOrder.Amount - orderBook.SellOrders[i].Amount
                        orderBook.RemoveSellOrder(orderBook.SellOrders, i) 
            if BuyOrder.Amount == 0:
                orderBook.RemoveBuyOrder(orderBook.BuyOrders, m)
            print("Limit Buy Order " + BuyOrder.ID +  " has been processed")
        else:
            Cancel = CancelOrder()
            Cancel.CancelBuyOrder(BuyOrder, orderBook.BuyOrders, m)
    
    def ProcessSellOrder(self, SellOrder, BuyOrders, m):
# We will build functions to process limit orders and market orders. We will consider both the possibility of a 
# fill of the entire order and a partial fill.
        if SellOrder.Type == 1:
            n = len(BuyOrders)
            index = n-1
            for o in reversed(range(n)):
                if BuyOrders[o].Price > SellOrder.Price:
                    break
                else:
                    index = index - 1 
            print(index)
            if BuyOrders[index].Price < SellOrder.Price:
                print("No Order has been processed")
            else:
                if BuyOrders[index].Amount == SellOrder.Amount:
                    Transactions.BuyTransaction(BuyOrders[index], transactionBook)
                    Transactions.SellTransaction(SellOrder, transactionBook)
                    orderBook.RemoveBuyOrder(orderBook.BuyOrders, index)
                elif BuyOrders[index].Amount > SellOrder.Amount: 
                    BuyTransaction = copy.deepcopy(orderBook.BuyOrders[index])
                    BuyTransaction.Amount = SellOrder.Amount
                    SellTransaction = copy.deepcopy(SellOrder)
                    Transactions.BuyTransaction(BuyTransaction, transactionBook)
                    Transactions.SellTransaction(SellTransaction, transactionBook)
                    orderBook.BuyOrders[index].Amount = orderBook.BuyOrders[index].Amount - SellOrder.Amount
                else:
                    SellTransaction = copy.deepcopy(SellOrder)
                    SellTransaction.Amount = BuyOrders[index].Amount
                    SellTransaction.Price = BuyOrders[index].Price
                    Transactions.BuyTransaction(orderBook.BuyOrders[index], transactionBook)
                    Transactions.SellTransaction(SellTransaction, transactionBook)
                    SellOrder.Amount = SellOrder.Amount - orderBook.BuyOrders[index].Amount
                    orderBook.RemoveBuyOrder(orderBook.BuyOrders, index)
                    index = index - 1
                    while SellOrder.Amount > 0:
                        for o in reversed(range(index+1)):
                            if BuyOrders[o].Price > SellOrder.Price:
                                break
                            else:
                                index = index - 1
                        if BuyOrders[index].Price < SellOrder.Price:
                            break
                        else:
                            if BuyOrders[index].Amount == SellOrder.Amount:
                                Transactions.SellTransaction(SellOrder, transactionBook)
                                Transactions.BuyTransaction(BuyOrders[index], transactionBook)
                                orderBook.RemoveBuyOrder(orderBook.BuyOrders, index)
                                SellOrder.Amount = 0
                            elif BuyOrders[index].Amount > SellOrder.Amount: 
                                BuyTransaction = copy.deepcopy(orderBook.BuyOrders[index])
                                BuyTransaction.Amount = SellOrder.Amount
                                SellTransaction = copy.deepcopy(SellOrder)
                                Transactions.BuyTransaction(BuyTransaction, transactionBook)
                                Transactions.SellTransaction(SellTransaction, transactionBook)
                                orderBook.BuyOrders[index].Amount = orderBook.BuyOrders[index].Amount - SellOrder.Amount 
                                SellOrder.Amount = 0
                            else:
                                SellTransaction = copy.deepcopy(SellOrder)
                                SellTransaction.Amount = BuyOrders[index].Amount
                                SellTransaction.Price = BuyOrders[index].Price
                                Transactions.BuyTransaction(orderBook.BuyOrders[index], transactionBook)
                                Transactions.SellTransaction(SellTransaction, transactionBook)
                                SellOrder.Amount = SellOrder.Amount - orderBook.BuyOrders[index].Amount
                                orderBook.RemoveBuyOrder(orderBook.BuyOrders, index)
                                index = index - 1
            if SellOrder.Amount == 0:
                orderBook.RemoveSellOrder(orderBook.SellOrders, m)
        elif SellOrder.Type == 0:
            while SellOrder.Amount > 0:
                for i in range(len(BuyOrders)):
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
            print("Market Sell Order " + SellOrder.ID +  " has been processed")
        else:
            Cancel = CancelOrder()
            Cancel.CancelSellOrder(SellOrder, orderBook.SellOrders, m)
            
class CancelOrder:

# The following code is meant to process cancel buy and sell orders, both full and partial.

    def CancelBuyOrder(self, BuyOrder, BuyOrders, m):
        for i in range(len(BuyOrders)):
            if BuyOrders[i].ID == BuyOrder.ID:
                if BuyOrders[i].Amount == BuyOrder.Amount:
                    print("Buy Order " + BuyOrders[i].ID + " has been canceled"  )
                    orderBook.RemoveBuyOrder(orderBook.BuyOrders, i)
                    orderBook.RemoveBuyOrder(orderBook.BuyOrders, m)
                    break
                else:
                    orderBook.BuyOrders[i].Amount = orderBook.BuyOrders[i].Amount - BuyOrder.Amount 
                    orderBook.RemoveBuyOrder(orderBook.BuyOrders, m)
                    break
                    
    def CancelSellOrder(self, SellOrder, SellOrders, m):
        for i in range(len(SellOrders)):
            if SellOrders[i].ID == SellOrder.ID:
                if SellOrders[i].Amount == SellOrder.Amount:
                    print("Sell Order" + SellOrders[i].ID + " has been canceled"  )
                    orderBook.RemoveSellOrder(orderBook.SellOrders, i)
                    orderBook.RemoveBuyOrder(orderBook.BuyOrders, m)
                    break
                else:
                    orderBook.SellOrders[i].Amount = orderBook.SellOrders[i].Amount - SellOrder.Amount
                    orderBook.RemoveBuyOrder(orderBook.BuyOrders, m)
                    break
                    
                    
Process = ProcessOrder()  

m = len(orderBook.SellOrders) - 1

Process.ProcessSellOrder(orderBook.SellOrders[m], orderBook.BuyOrders, m)
            
print("BuyOrders:" + str(len(orderBook.BuyOrders)))
for o in orderBook.BuyOrders:
    o.printOrder()

print("SellOrders:" + str(len(orderBook.SellOrders)))
for o in orderBook.SellOrders:
    o.printOrder()
    
print("TransactionBook:" + str(len(transactionBook)))
for o in transactionBook:
    o.printOrder()
