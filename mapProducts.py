import random

def map_products(dict_by_format):
    dict_keys_map = {
            "name": "name",
            "image": "url",
            "sku": "id",
            "manufacturer": "manufacturer",
            "modelNumber": "modelNumber",
            "longDescription": "description",
            "salePrice": "price",
            "categoryPath": "category"
        } 
    dict_formated = dict((dict_keys_map[key], value) for (key, value) in dict_by_format.items()) 
    dict_formated["category"] = dict_formated["category"][2]["name"]
    dict_formated["stock"] = random.randint(1, 20)
    return dict_formated

def map_list_products(products):
    list_products = [map_products(product) for product in products]
    list_categories = list(set([product['category'] for product in list_products]))
    # list_categories = [{'name': category, 'value': True}  for category in list_categories]
    return list_products, list_categories