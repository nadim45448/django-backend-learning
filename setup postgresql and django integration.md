# PostgreSQL Setup and Django Integration

This guide contains the commands used to install PostgreSQL, create a database and user, configure permissions, test PostgreSQL, and connect a Django project to PostgreSQL.

---

# 1. Install PostgreSQL

Update package information:

```bash
sudo apt update
```

Install PostgreSQL:

```bash
sudo apt install postgresql postgresql-contrib
```

Check PostgreSQL status:

```bash
sudo systemctl status postgresql
```

If it is not running:

```bash
sudo systemctl start postgresql
```

Enable PostgreSQL to start automatically:

```bash
sudo systemctl enable postgresql
```

---

# 2. Open PostgreSQL

Switch to the PostgreSQL system user:

```bash
sudo -u postgres psql
```

You should see:

```text
postgres=#
```

---

# 3. Check Existing Databases

Inside PostgreSQL:

```sql
\l
```

or:

```sql
\list
```

Example:

```text
Name      | Owner
----------+----------
postgres  | postgres
template0 | postgres
template1 | postgres
```

---

# 4. Create a PostgreSQL User

Create the application user:

```sql
CREATE USER myproject_user WITH PASSWORD 'your_password';
```

Replace:

```text
your_password
```

with your actual password.

---

# 5. Create the Django Database

Create:

```sql
CREATE DATABASE myproject_db;
```

---

# 6. Give the User Access to the Database

```sql
GRANT ALL PRIVILEGES ON DATABASE myproject_db TO myproject_user;
```

Check databases:

```sql
\l
```

You should see something similar to:

```text
myproject_db | postgres
```

---

# 7. Connect to the Django Database

From the Linux terminal:

```bash
psql -U myproject_user -d myproject_db -h localhost
```

Enter the password.

Successful connection:

```text
myproject_db=>
```

---

# 8. Check Current User

Inside PostgreSQL:

```sql
SELECT current_user;
```

Example:

```text
current_user
--------------
myproject_user
```

---

# 9. Check Current Database

```sql
SELECT current_database();
```

Expected:

```text
current_database
------------------
myproject_db
```

---

# 10. Check PostgreSQL Version

```sql
SELECT version();
```

Or from Linux:

```bash
psql --version
```

Example:

```text
psql (PostgreSQL) 16.15
```

---

# 11. PostgreSQL Schemas

Check schemas:

```sql
\dn
```

The main schema we used is:

```text
public
```

---

# 12. Check Schema Permissions

```sql
\dn+
```

You may see permissions associated with the `public` schema.

---

# 13. Grant Schema Permissions

If the application user doesn't have permission to create tables:

```sql
GRANT USAGE, CREATE ON SCHEMA public TO myproject_user;
```

If necessary, connect as the database owner/postgres user and grant the permissions there.

Check the current user:

```sql
SELECT current_user;
```

---

# 14. Create a Test Table

We used this table to practice SQL:

```sql
CREATE TABLE test_product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price INTEGER
);
```

Check tables:

```sql
\dt
```

---

# 15. Insert Data

Insert the first product:

```sql
INSERT INTO test_product (name, price)
VALUES ('Laptop', 800);
```

Insert another:

```sql
INSERT INTO test_product (name, price)
VALUES ('Mouse', 20);
```

Insert another:

```sql
INSERT INTO test_product (name, price)
VALUES ('Keyboard', 50);
```

---

# 16. Read Data

```sql
SELECT * FROM test_product;
```

Expected:

```text
id | name     | price
---+----------+------
1  | Laptop   | 800
2  | Mouse    | 20
3  | Keyboard | 50
```

---

# 17. Filtering

```sql
SELECT * FROM test_product
WHERE price > 50;
```

Multiple conditions:

```sql
SELECT * FROM test_product
WHERE price > 20 AND price < 800;
```

Using OR:

```sql
SELECT * FROM test_product
WHERE price < 30 OR price > 700;
```

Using IN:

```sql
SELECT * FROM test_product
WHERE price IN (20, 50);
```

---

# 18. Update Data

```sql
UPDATE test_product
SET price = 25
WHERE id = 2;
```

Verify:

```sql
SELECT * FROM test_product;
```

Always be careful with `UPDATE`.

This:

```sql
UPDATE test_product
SET price = 25;
```

updates every row because there is no `WHERE`.

---

# 19. Delete Data

Delete one row:

```sql
DELETE FROM test_product
WHERE id = 3;
```

Be careful with:

```sql
DELETE FROM test_product;
```

This deletes all rows from the table.

---

# 20. Sorting

Ascending:

```sql
SELECT * FROM test_product
ORDER BY price ASC;
```

Descending:

```sql
SELECT * FROM test_product
ORDER BY price DESC;
```

---

# 21. Limit Results

Get the two most expensive products:

```sql
SELECT * FROM test_product
ORDER BY price DESC
LIMIT 2;
```

---

# 22. Counting

Count all products:

```sql
SELECT COUNT(*) FROM test_product;
```

Count products over a certain price:

```sql
SELECT COUNT(*)
FROM test_product
WHERE price > 50;
```

---

# 23. Aggregation

Total:

```sql
SELECT SUM(price)
FROM test_product;
```

Average:

```sql
SELECT AVG(price)
FROM test_product;
```

Minimum:

```sql
SELECT MIN(price)
FROM test_product;
```

Maximum:

```sql
SELECT MAX(price)
FROM test_product;
```

---

# 24. GROUP BY

Example:

```sql
SELECT customer_id, COUNT(*)
FROM test_order
GROUP BY customer_id;
```

`GROUP BY` creates groups before applying aggregate functions such as `COUNT()`.

---

# 25. HAVING

Filter grouped results:

```sql
SELECT
    customer_id,
    COUNT(*) AS total_orders
FROM test_order
GROUP BY customer_id
HAVING COUNT(*) > 1;
```

Remember:

```text
WHERE
→ filters individual rows

HAVING
→ filters groups
```

---

# 26. Create a Customer Table

For practicing relationships:

```sql
CREATE TABLE test_customer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);
```

Insert customers:

```sql
INSERT INTO test_customer (name)
VALUES ('Nadim');

INSERT INTO test_customer (name)
VALUES ('Rahim');

INSERT INTO test_customer (name)
VALUES ('Karim');
```

Check:

```sql
SELECT * FROM test_customer;
```

---

# 27. Create an Order Table

```sql
CREATE TABLE test_order (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES test_customer(id),
    product_id INTEGER REFERENCES test_product(id)
);
```

Here:

```text
customer_id
→ references test_customer(id)

product_id
→ references test_product(id)
```

This creates foreign-key relationships.

---

# 28. Insert Orders

```sql
INSERT INTO test_order (customer_id, product_id)
VALUES (1, 1);

INSERT INTO test_order (customer_id, product_id)
VALUES (1, 2);

INSERT INTO test_order (customer_id, product_id)
VALUES (2, 3);
```

Check:

```sql
SELECT * FROM test_order;
```

---

# 29. INNER JOIN

```sql
SELECT
    test_order.id,
    test_customer.name AS customer,
    test_product.name AS product
FROM test_order
INNER JOIN test_customer
    ON test_order.customer_id = test_customer.id
INNER JOIN test_product
    ON test_order.product_id = test_product.id;
```

`INNER JOIN` returns matching records.

---

# 30. LEFT JOIN

Show every customer, including customers without orders:

```sql
SELECT
    test_customer.name AS customer,
    test_order.id AS order_id
FROM test_customer
LEFT JOIN test_order
    ON test_customer.id = test_order.customer_id;
```

A customer without an order will have:

```text
NULL
```

for `order_id`.

---

# 31. Transactions

Start a transaction:

```sql
BEGIN;
```

Make a change:

```sql
UPDATE test_product
SET price = 999
WHERE id = 1;
```

Check:

```sql
SELECT * FROM test_product;
```

Undo the change:

```sql
ROLLBACK;
```

Verify:

```sql
SELECT * FROM test_product;
```

The old value should return.

---

# 32. Commit a Transaction

Start:

```sql
BEGIN;
```

Update:

```sql
UPDATE test_product
SET price = 100
WHERE id = 2;
```

Save permanently:

```sql
COMMIT;
```

---

# 33. Inspect a Table

```sql
\d test_product
```

This shows information about the table, including columns, constraints, and indexes.

---

# 34. Inspect All Tables

```sql
\dt
```

---

# 35. Inspect Indexes

```sql
\d test_product
```

Look at the `Indexes` section.

---

# 36. Create an Index

```sql
CREATE INDEX product_name_index
ON test_product(name);
```

Then inspect:

```sql
\d test_product
```

---

# 37. Exit PostgreSQL

```sql
\q
```

---

# Django + PostgreSQL Integration

Now we connect the actual Django project to PostgreSQL.

---

# 38. Activate Django Virtual Environment

From the project directory:

```bash
source .venv/bin/activate
```

You should see:

```text
(.venv)
```

---

# 39. Install PostgreSQL Python Driver

```bash
pip install psycopg
```

Verify:

```bash
pip show psycopg
```

---

# 40. Configure Django `settings.py`

Open:

```text
your_project/settings.py
```

Find:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Replace it with:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myproject_db',
        'USER': 'myproject_user',
        'PASSWORD': 'YOUR_POSTGRES_PASSWORD',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Replace:

```text
YOUR_POSTGRES_PASSWORD
```

with the password of `myproject_user`.

---

# 41. Test Django Configuration

Run:

```bash
python manage.py check
```

Expected:

```text
System check identified no issues (0 silenced).
```

---

# 42. Create Django Migrations

If you changed your models:

```bash
python manage.py makemigrations
```

---

# 43. Apply Django Migrations to PostgreSQL

```bash
python manage.py migrate
```

Django now creates its database tables inside:

```text
myproject_db
```

---

# 44. Verify Django Tables from PostgreSQL

Connect:

```bash
psql -U myproject_user -d myproject_db -h localhost
```

Then:

```sql
\dt
```

You should see Django tables such as:

```text
auth_user
django_admin_log
django_content_type
django_migrations
django_session
```

and your application's tables.

---

# 45. Check Django Migration History

```sql
SELECT * FROM django_migrations;
```

This shows which Django migrations have been applied.

---

# 46. Verify Django's Database Connection

Start Django shell:

```bash
python manage.py shell
```

Import the connection:

```python
from django.db import connection
```

Check the database backend:

```python
connection.vendor
```

Expected:

```text
'postgresql'
```

Check database name:

```python
connection.settings_dict["NAME"]
```

Expected:

```text
'myproject_db'
```

Check host:

```python
connection.settings_dict["HOST"]
```

Expected:

```text
'localhost'
```

Check port:

```python
connection.settings_dict["PORT"]
```

Expected:

```text
'5432'
```

---

# 47. Check Django ORM SQL

Import your model:

```python
from myapp.models import Product
```

Create a QuerySet:

```python
queryset = Product.objects.all()
```

Print the generated SQL:

```python
print(queryset.query)
```

This lets you see the SQL Django ORM generates.

---

# 48. Create Data Through Django ORM

```python
product = Product.objects.create(
    name="PostgreSQL Laptop",
    price=1000
)
```

Check:

```python
Product.objects.all()
```

---

# 49. Verify Django Data Directly in PostgreSQL

Exit Django shell:

```python
exit()
```

Connect to PostgreSQL:

```bash
psql -U myproject_user -d myproject_db -h localhost
```

Find your application's table:

```sql
\dt
```

Then query the Product table.

For example:

```sql
SELECT * FROM myapp_product;
```

Replace `myapp_product` with the actual table name shown by:

```sql
\dt
```

You should see the product created through Django.

---

# 50. Complete Architecture

After integration, the flow is:

```text
Python / Django Application
            ↓
       Django ORM
            ↓
       SQL Query
            ↓
          psycopg
            ↓
       PostgreSQL
            ↓
       myproject_db
            ↓
          Tables
            ↓
           Data
```

For example:

```python
Product.objects.all()
```

conceptually becomes:

```sql
SELECT *
FROM myapp_product;
```

PostgreSQL executes the SQL and Django converts the result back into Python objects.

---

# 51. Useful PostgreSQL Commands Cheat Sheet

| Command                      | Purpose                     |
| ---------------------------- | --------------------------- |
| `\l`                         | List databases              |
| `\c database_name`           | Connect to a database       |
| `\dt`                        | List tables                 |
| `\d table_name`              | Describe a table            |
| `\dn`                        | List schemas                |
| `\du`                        | List PostgreSQL users/roles |
| `\q`                         | Exit PostgreSQL             |
| `\?`                         | PostgreSQL command help     |
| `SELECT current_user;`       | Show current user           |
| `SELECT current_database();` | Show current database       |
| `SELECT version();`          | Show PostgreSQL version     |

---

# 52. Essential Linux PostgreSQL Commands

Check PostgreSQL:

```bash
sudo systemctl status postgresql
```

Start:

```bash
sudo systemctl start postgresql
```

Stop:

```bash
sudo systemctl stop postgresql
```

Restart:

```bash
sudo systemctl restart postgresql
```

Enable at startup:

```bash
sudo systemctl enable postgresql
```

Check version:

```bash
psql --version
```

Connect:

```bash
psql -U myproject_user -d myproject_db -h localhost
```

---

# 53. Important Concepts to Remember

### Database

A container that stores tables and other database objects.

### Table

Stores structured data in rows and columns.

### Primary Key

Uniquely identifies a row.

### Foreign Key

Creates a relationship between tables.

### Constraint

Protects data integrity.

### Index

Helps PostgreSQL find data efficiently.

### Transaction

Groups multiple database operations into one unit.

```text
BEGIN
   ↓
Operations
   ↓
COMMIT
```

or:

```text
BEGIN
   ↓
Operations
   ↓
ROLLBACK
```

### Django ORM

Allows Python code to interact with the database without manually writing SQL for every operation.

```python
Product.objects.all()
```

### PostgreSQL

The actual database system that stores and processes the data.

---

# Final Connection

The most important thing to remember from this entire phase is:

```text
Django Model
     ↓
Migration
     ↓
Database Table
     ↓
PostgreSQL
```

And:

```text
Django ORM
     ↓
SQL
     ↓
PostgreSQL
     ↓
Data
```

You have now completed the **PostgreSQL fundamentals + Django PostgreSQL integration phase**.
