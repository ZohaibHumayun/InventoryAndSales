This is Inventory and Sales management backend API developed with fastAPI and python

SQL queries for the following tasks:
------------------------------------

**Daily sales**

select sum(SalesWithTax) from sales where cast(createdAt as Date) = cast(CURRENT_DATE as Date)

**Weekly sales**

select SUM(SalesWithTax) from sales where cast(createdAt as Date) > now() - INTERVAL 7 day

**Current Monthly sales**

SELECT SUM(SalesWithTax) FROM sales WHERE cast(createdAt as Date) >= (LAST_DAY(NOW()) + INTERVAL 1 DAY - INTERVAL 1 MONTH) AND cast(createdAt as Date) < (LAST_DAY(NOW()) + INTERVAL 1 DAY)

**Monthly Sales**

SELECT SUM(SalesWithTax) FROM sales WHERE CONCAT(YEAR(cast(createdAt as Date)),'-',MONTH(cast(createdAt as Date))) = '2023-10'

**Yearly Sales**

SELECT SUM(SalesWithTax) FROM sales WHERE CONCAT(YEAR(cast(createdAt as Date))) = '2023'

**Compare revenues accross Quaters**

SELECT SUM(SalesWithTax), QUARTER(cast(createdAt as Date)) as Quarter
FROM sales        
WHERE QUARTER(cast(createdAt as Date)) = 4

**Compare revenues accross categories**

select category.Name, SUM(sales.SalesWithTax) as Sales from sales join category_product using (ProductID) join category USING (CategoryID) GROUP BY category.Name

**Product wise sales**

select product.Discription, SUM(sales.SalesWithTax) as Sales from sales join category_product using (ProductID) join product USING (ProductID) GROUP BY product.Discription

**Current inventory status**

SELECT discription, QuantityOnHand from product

**Low Stock status**

SELECT Discription, QuantityOnHand FROM product where QuantityOnHand <= 5

**Updating quantity in hand by minus one after selling **

UPDATE product SET QuantityOnHand = QuantityOnHand -1 WHERE ProductID = 1

