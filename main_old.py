# uvicorn main:app --reload
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response

import requests
from typing import Union
import schedule
import time
import threading
import mapProducts

from pydantic import BaseModel
from typing import List

from fastapi.middleware.cors import CORSMiddleware

import json


PRODUCTS = "products.json"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Definir una tarea programada que se ejecutará cada x tiempo
    print("Startup")
    start_thread()
    yield
    stop_thread()
    
app = FastAPI(lifespan=lifespan)


class Product(BaseModel):
    name: str
    url: str
    id: int
    manufacturer: str
    modelNumber: str
    description: str
    price: float
    category: str
    stock: int


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir acceso desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/products")
def get_products(response: Response):
    with open(PRODUCTS, "r") as file:
        data = json.load(file)
        
    response.headers["Access-Control-Allow-Origin"] = "*"
    return data

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/products")
def update_products(products: List[Product]):
    with open(PRODUCTS, "r") as file:
        data = json.load(file)
    productos = data["products"]
    categories = data["categories"]
     
    for product in products:
        index = next((i for i, p in enumerate(productos) if p["id"] == product.id), None)
        if index is not None:
            productos[index] = product.dict()
        else:
            productos.append(product.dict())
    
    with open(PRODUCTS, "w") as file:
        json.dump({"products": productos, "categories": categories}, file)
            
    return data

class thread_load_products(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(thread_load_products, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while True:
            if self.stopped():
                return
            desktop_all_in_one_computers = requests.get("https://api.bestbuy.com/v1/products(inStoreAvailability=true&(categoryPath.id=abcat0501000))?apiKey=AAWiC1QKpJnP2Fm0DjGv4G9k&sort=name.asc&show=name,image,sku,manufacturer,modelNumber,longDescription,salePrice,categoryPath.name,&pageSize=5&format=json")
            products = desktop_all_in_one_computers.json()["products"]
            
            digital_cameras = requests.get("https://api.bestbuy.com/v1/products(inStoreAvailability=true&(categoryPath.id=abcat0401000))?apiKey=AAWiC1QKpJnP2Fm0DjGv4G9k&sort=name.asc&show=name,image,sku,manufacturer,modelNumber,longDescription,salePrice,categoryPath.name&pageSize=5&format=json")
            products.extend(digital_cameras.json()["products"])
            
            all_cell_phones = requests.get("https://api.bestbuy.com/v1/products(inStoreAvailability=true&(categoryPath.id=pcmcat209400050001))?apiKey=AAWiC1QKpJnP2Fm0DjGv4G9k&sort=name.asc&show=name,image,sku,manufacturer,modelNumber,longDescription,salePrice,categoryPath.name&pageSize=5&format=json")
            products.extend(all_cell_phones.json()["products"])
            
            headphones = requests.get("https://api.bestbuy.com/v1/products(inStoreAvailability=true&(categoryPath.id=abcat0204000))?apiKey=AAWiC1QKpJnP2Fm0DjGv4G9k&sort=name.asc&show=name,image,sku,manufacturer,modelNumber,longDescription,salePrice,categoryPath.name&pageSize=5&format=json")
            products.extend(headphones.json()["products"])
            
            home_audio = requests.get("https://api.bestbuy.com/v1/products(inStoreAvailability=true&(categoryPath.id=pcmcat241600050001))?apiKey=AAWiC1QKpJnP2Fm0DjGv4G9k&sort=name.asc&show=name,image,sku,manufacturer,modelNumber,longDescription,salePrice,categoryPath.name&pageSize=5&format=json")
            products.extend(home_audio.json()["products"])
            
            home_automation_security = requests.get("https://api.bestbuy.com/v1/products(inStoreAvailability=true&(categoryPath.id=pcmcat254000050002))?apiKey=AAWiC1QKpJnP2Fm0DjGv4G9k&sort=name.asc&show=name,image,sku,manufacturer,modelNumber,longDescription,salePrice,categoryPath.name&pageSize=5&format=json")
            products.extend(home_automation_security.json()["products"])
            
            ipad_tablets_e_readers = requests.get("https://api.bestbuy.com/v1/products(inStoreAvailability=true&(categoryPath.id=pcmcat209000050006))?apiKey=AAWiC1QKpJnP2Fm0DjGv4G9k&sort=name.asc&show=name,image,sku,manufacturer,modelNumber,longDescription,salePrice,categoryPath.name&pageSize=5&format=json")
            products.extend(ipad_tablets_e_readers.json()["products"])
            
            laptops = requests.get("https://api.bestbuy.com/v1/products(inStoreAvailability=true&(categoryPath.id=abcat0502000))?apiKey=AAWiC1QKpJnP2Fm0DjGv4G9k&sort=name.asc&show=name,image,sku,manufacturer,modelNumber,longDescription,salePrice,categoryPath.name&pageSize=5&format=json")
            products.extend(laptops.json()["products"])
            
            portable_wireless_speakers = requests.get("https://api.bestbuy.com/v1/products(inStoreAvailability=true&(categoryPath.id=pcmcat310200050004))?apiKey=AAWiC1QKpJnP2Fm0DjGv4G9k&sort=name.asc&show=name,image,sku,manufacturer,modelNumber,longDescription,salePrice,categoryPath.name&pageSize=5&format=json")
            products.extend(portable_wireless_speakers.json()["products"])
            
            refrigerators = requests.get("https://api.bestbuy.com/v1/products(inStoreAvailability=true&(categoryPath.id=abcat0901000))?apiKey=AAWiC1QKpJnP2Fm0DjGv4G9k&sort=name.asc&show=name,image,sku,manufacturer,modelNumber,longDescription,salePrice,categoryPath.name&pageSize=5&format=json")
            products.extend(refrigerators.json()["products"])
            
            tvs = requests.get("https://api.bestbuy.com/v1/products(inStoreAvailability=true&(categoryPath.id=abcat0101000))?apiKey=AAWiC1QKpJnP2Fm0DjGv4G9k&sort=name.asc&show=name,image,sku,manufacturer,modelNumber,longDescription,salePrice,categoryPath.name&pageSize=5&format=json")
            products.extend(tvs.json()["products"])
            
            products_formated, categories = mapProducts.map_list_products(products);
            
            with open("products.json", "w") as file:
                json.dump({"products": products_formated, "categories": categories}, file)
            print("Productos Obtenidos de Buy Best")
            time.sleep(3600*24)

x = thread_load_products()

def start_thread():
    x.start()
    
def stop_thread():
    x.stop()
    x.join()

