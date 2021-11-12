import sys
import json
import os
from pprint import pprint

__db_location__ = "db"
__session_file__ = f"{__db_location__}/session.db"
__item_folder__ = f"{__db_location__}/item"
__item__last_id__ = f"{__db_location__}/item_id.db"


def init(arguments):

    def db():
        os.makedirs(__item_folder__)

    section = arguments[0]
    if section == "init":
        command = arguments[1]
        if command == "db":
            db()


def __get_logged_user():
    f = open(__session_file__, "r")
    username = f.readline()
    return username


def view():
    username = __get_logged_user()
    print(username)


def login(username):
    f = open(__session_file__, "w")
    f.write(username)
    f.close()


class Item:
    def __init__(self):
        if os.path.exists(__item__last_id__):
            with open(__item__last_id__, "r") as last_id_f:
                self.last_id = int(last_id_f.readline())
        else:
            self.last_id = 0

    def save(self):
        id = self.last_id+1

        # Save database item
        _data_ = {
            "id": id,
            "name": self.name,
            "price": self.price,
            "sellingPrice": self.selling_price
        }
        with open(f"{__item_folder__}/{id}.db", "w") as item_file:
            json.dump(_data_, item_file)

        # Save next id
        self.last_id += 1
        with open(__item__last_id__, "w") as f:
            f.write(str(self.last_id))

    def find(self, id):
        Item.__get_item_by_path(self, f"{__item_folder__}/{id}.db")

    def __get_item_by_path(item, path):
        with open(path, "r") as item_file:
            _data_ = json.load(item_file)
            item.id = _data_["id"]
            item.name = _data_["name"]
            item.price = _data_["price"]
            item.selling_price = _data_["sellingPrice"]

    def all(self):
        item_file_names = os.listdir(__item_folder__)
        items = []
        for item_file_name in item_file_names:
            item = Item()
            Item.__get_item_by_path(
                item, f"{__item_folder__}/{item_file_name}")
            items.append(item)
        return items

    def search(self, key, value):
        items = self.all()
        result_items = []
        for item in items:
            item_value = getattr(item,key)
            if item_value == value:
                result_items.append(item)
        return result_items


    def __repr__(self):
        return f"id:{self.id},name:{self.name},price:{self.price}"

    def __str__(self):
        return f"id:{self.id},name:{self.name},price:{self.price}"


def item_create(name, price, selling_price):
    item = Item()
    item.name = name
    item.price = price
    item.selling_price = selling_price
    item.save()


def item_all():
    item = Item()
    items = item.all()
    pprint(items)

def item_view(id):
    item = Item()
    item.find(id)
    print(item.id, item.name, item.price, item.selling_price)

def item_search(key,value):
    item = Item()
    results = item.search(key,value)
    pprint(results)


if __name__ == "__main__":
    arguments = sys.argv[1:]

    init(arguments)

    section = arguments[0]
    command = arguments[1]
    params = arguments[2:]

    if section == "user":
        if command == "login":
            login(*params)
        elif command == "view":
            view()
    elif section == "item":
        if command == "create":
            item_create(*params)
        elif command == "all":
            item_all()
        elif command == "view":
            item_view(*params)
        elif command == "search":
            item_search(*params)

