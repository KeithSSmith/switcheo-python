from socketio import ClientNamespace as SocketIOClientNamespace
from operator import itemgetter
from switcheo.utils import stringify_message, sha1_hash_digest
import threading


class OrderBooksNamespace(SocketIOClientNamespace):
    
    def __init__(self):
        self.lock = threading.Lock()
        self.namespace = '/v2/books'
        self.order_book = {}
        SocketIOClientNamespace.__init__(self, namespace=self.namespace)
    
    def on_connect(self):
        pass
    
    def on_disconnect(self):
        pass
    
    def on_join(self):
        pass
    
    def on_all(self, data):
        self.lock.acquire()
        self.order_book[data["room"]["pair"]] = data
        self.lock.release()
        digest_hash = data["digest"]
        book = data["book"]
        book_digest_hash = sha1_hash_digest(stringify_message(book))
        if digest_hash != book_digest_hash:
            self.emit(event="leave", data=data["room"], namespace='/v2/books')
            self.emit(event="join", data=data["room"], namespace='/v2/books')
    
    def on_updates(self, data):
        update_digest = data["digest"]
        update_pair = data["room"]["pair"]
        update_events = data["events"]
        buy_event = False
        sell_event = False
        if "symbol" in self.order_book[update_pair]["book"]:
            del self.order_book[update_pair]["book"]["symbol"]
        self.lock.acquire()
        for event in update_events:
            price_match = False
            event_iteration = 0
            if event["side"] == "buy":
                event_side = "buys"
                buy_event = True
            elif event["side"] == "sell":
                event_side = "sells"
                sell_event = True
            event_price = event["price"]
            event_change = event["delta"]
            for side in self.order_book[update_pair]["book"][event_side]:
                if side["price"] == event_price:
                    price_match = True
                    updated_amount = int(side["amount"]) + int(event_change)
                    if updated_amount == 0:
                        self.order_book[update_pair]["book"][event_side].remove(side)
                    else:
                        updated_book = {}
                        updated_book["amount"] = str(updated_amount)
                        updated_book["price"] = str(event_price)
                        self.order_book[update_pair]["book"][event_side][event_iteration] = updated_book
                    break
                event_iteration += 1
            if not price_match:
                new_book = {}
                new_book["amount"] = event_change
                new_book["price"] = event_price
                self.order_book[update_pair]["book"][event_side].append(new_book)
        if buy_event and sell_event:
            self.order_book[update_pair]["book"]["buys"] = sorted(
                self.order_book[update_pair]["book"]["buys"], key=itemgetter("price"), reverse=True)
            self.order_book[update_pair]["book"]["sells"] = sorted(
                self.order_book[update_pair]["book"]["sells"], key=itemgetter("price"), reverse=True)
        elif buy_event:
            self.order_book[update_pair]["book"]["buys"] = sorted(
                self.order_book[update_pair]["book"]["buys"], key=itemgetter("price"), reverse=True)
        elif sell_event:
            self.order_book[update_pair]["book"]["sells"] = sorted(
                self.order_book[update_pair]["book"]["sells"], key=itemgetter("price"), reverse=True)
        book = self.order_book[update_pair]["book"]
        self.lock.release()
        book_digest_hash = sha1_hash_digest(stringify_message(book))
        if update_digest != book_digest_hash:
            self.emit(event="leave", data=data["room"], namespace='/v2/books')
            self.emit(event="join", data=data["room"], namespace='/v2/books')


class TradeEventsNamespace(SocketIOClientNamespace):

    def __init__(self):
        self.lock = threading.Lock()
        self.namespace = '/v2/trades'
        self.trade_events = {}
        SocketIOClientNamespace.__init__(self, namespace=self.namespace)

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_join(self):
        pass

    def on_all(self, data):
        self.lock.acquire()
        self.trade_events[data["room"]["pair"]] = data
        self.lock.release()
        digest_hash = data["digest"]
        trades = data["trades"]
        trade_digest_hash = sha1_hash_digest(stringify_message(trades))
        if digest_hash != trade_digest_hash:
            self.emit(event="leave", data=data["room"], namespace='/v2/trades')
            self.emit(event="join", data=data["room"], namespace='/v2/trades')

    def on_updates(self, data):
        update_digest = data["digest"]
        update_pair = data["room"]["pair"]
        update_events = data["events"]
        update_limit = data["limit"]
        self.lock.acquire()
        self.trade_events[update_pair]["trades"] = update_events + \
            self.trade_events[update_pair]["trades"]
        trade_slice = update_limit - 1
        self.trade_events[update_pair]["trades"] = self.trade_events[update_pair]["trades"][0:trade_slice]
        trades = self.trade_events[update_pair]["trades"]
        self.lock.release()
        trade_digest_hash = sha1_hash_digest(stringify_message(trades))
        if update_digest != trade_digest_hash:
            self.emit(event="leave", data=data["room"], namespace='/v2/trades')
            self.emit(event="join", data=data["room"], namespace='/v2/trades')


class OrderEventsNamespace(SocketIOClientNamespace):

    def __init__(self):
        self.lock = threading.Lock()
        self.namespace = '/v2/orders'
        self.order_events = {}
        SocketIOClientNamespace.__init__(self, namespace=self.namespace)

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_join(self):
        pass

    def on_all(self, data):
        self.lock.acquire()
        self.order_events = data
        self.lock.release()

    def on_updates(self, data):
        update_events = data["events"]
        self.lock.acquire()
        self.order_events["orders"] + update_events
        self.lock.release()
