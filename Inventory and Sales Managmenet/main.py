import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import mysql.connector as mc
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()

# Pydantic model to define the schema of the data
class Item(BaseModel):
    name: str
    description: str = None

class Product(BaseModel):
    Discription: str
    ListPrice : int
    QuantityOnHand : int
    Weight : int
    PurchasePrice : int

class ProductSpecial(BaseModel):
    QuantityOnHand : int
    ProductID : int

class Sales(BaseModel):
    SalesBeforeTax : int
    TaxRate : int
    TotalTax : int
    SalesWithTax : int
    TransactionType : str

passw = ""
db_connection = mc.connect(host="localhost", user = "root", password = passw, port = 3307 )
curs = db_connection.cursor()
curs.execute("CREATE DATABASE IF NOT EXISTS SalesAndInventory")
db_connection.close()

#connecting to database
database_connection = mc.connect(host="localhost",database="SalesAndInventory",user = "root",password = passw, port = 3307)
cur = database_connection.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Products(
    PRODUCT_ID int PRIMARY KEY,
    PRODUCT_NAME varchar(255),
    SUPPLIER varchar(255),
    COST_PRICE int,
    SELLING_PRICE int,
    INVENTORY int,
    UNIQUE (PRODUCT_ID)
);""")

cur.execute("""CREATE TABLE IF NOT EXISTS `Users` (
	`UserID` INT,
	`UserName` VARCHAR(255),
    `Password` VARCHAR(255),
	`Role` VARCHAR(255),
    `Name` VARCHAR(255),
	PRIMARY KEY (`UserID`));""")

cur.execute("""CREATE TABLE IF NOT EXISTS `Customer` (
	`CustomerID` INT,
	`Cust_Name` VARCHAR(255),
    `Cust_Address` VARCHAR(255),
	`PhoneNo` VARCHAR(255),
    `Country` VARCHAR(255),
    `City` VARCHAR(255),
    `createdAt` DATETIME NOT NULL,
	PRIMARY KEY (`CustomerID`));""")

cur.execute("""CREATE TABLE IF NOT EXISTS `Product` (
	`ProductID` INT,
	`Discription` VARCHAR(255),
    `ListPrice` DOUBLE(5,4),
	`QuantityOnHand` int,
    `Weight` DOUBLE(5,4),
    `createdAt` DATETIME NOT NULL,
	PRIMARY KEY (`ProductID`));""")

cur.execute("""CREATE TABLE IF NOT EXISTS `Category` (
	`CategoryID` INT,
    `createdAt` DATETIME NOT NULL,
    `Name` VARCHAR(255),
	PRIMARY KEY (`CategoryID`));""")

cur.execute("""CREATE TABLE IF NOT EXISTS `Category_Product` (
	`CategoryID` INT,
    `ProductID` int,
    `createdAt` DATETIME NOT NULL,
	Constraint fk_category_id FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID),
    Constraint fk_product_id FOREIGN KEY (ProductID) REFERENCES Product(ProductID));""")

cur.execute("""CREATE TABLE IF NOT EXISTS `SALES` (
	`SalesID` INT,
    `CategoryID` INT,
	`TransactionType` VARCHAR(255),
    `SalesBeforeTax` DOUBLE(5,4),
	`TaxRate` DOUBLE(5,4),
    `TotalTax` DOUBLE(5,4),
    `SalesWithTax` DOUBLE(5,4),
    `createdAt` DATETIME NOT NULL,
	PRIMARY KEY (`SalesID`),
    Constraint fk_category_id FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID));""")

# Route to create an item 
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    cursor = cur
    query = "INSERT INTO items (name, description) VALUES (%s, %s)"
    cur.execute(query, (item.name, item.description))
    database_connection.commit()
    item.id = cur.lastrowid
    return item

# Route to create a new product registration
@app.post("/product/", response_model=Product)
def create_item(product: Product):
    cursor = cur
    query = "INSERT INTO Product (Discription, ListPrice, QuantityOnHand, Weight, PurchasePrice) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(query, (product.Discription, product.ListPrice, product.QuantityOnHand, product.Weight, product.PurchasePrice))
    database_connection.commit()
    return product

# Route to read an item
@app.get("/items/gett/{item_id}", response_model=Item)
def read_item(item_id: int):
    cursor = cur
    query = "SELECT id, name, description FROM items WHERE id=%s"
    cur.execute(query, (item_id,))
    item = cur.fetchone()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item[0], "name": item[1], "description": item[2]}

# Route to read an item of product
@app.get("/items/product/get/{ProductID}", response_model=Product)
def read_item(item_id: int):
    cursor = cur
    query = "SELECT Discription, ListPrice, QuantityOnHand, Weight, PurchasePrice FROM product WHERE ProductID=%s"
    cur.execute(query, (item_id,))
    item = cur.fetchone()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"Discription": item[0], "ListPrice": item[1], "QuantityOnHand": item[2]}

# Route to update an item of product
@app.put("/items/update/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    cursor = cur
    query = "UPDATE items SET name=%s, description=%s WHERE id=%s"
    cur.execute(query, (item.name, item.description, item_id))
    database_connection.commit()
    item.id = item_id
    return item

# Route to delete an item
@app.delete("/items/delete/{item_id}", response_model=Item)
def delete_item(item_id: int):
    cursor = cur
    query = "DELETE FROM items WHERE id=%s"
    cur.execute(query, (item_id,))
    database_connection.commit()
    return {"id": item_id}

                
