import uuid
import random
from datetime import datetime, timedelta

import psycopg2
from psycopg2.extras import execute_values
from faker import Faker


HOST = 'localhost' 
USER = 'postgres'
PASSWORD = 'admin123'
DATABASE = 'assignment_02'
PORT = '5432'


CLIENTS_COUNT = 100_000
PRODUCTS_COUNT = 10_000
ORDERS_COUNT = 1_000_000
CHUNK_SIZE = 10_000

fake = Faker()


def insert_clients(cursor):
    print("Inserting into clients...")

    client_insert_query = """
        INSERT INTO clients
            (id, name, surname, email, phone, address, status)
        VALUES %s
    """

    client_ids = []

    for start in range(0, CLIENTS_COUNT, CHUNK_SIZE):
        current_chunk_size = min(CHUNK_SIZE, CLIENTS_COUNT - start)

        clients_data = []
        for _ in range(current_chunk_size):
            client_id = str(uuid.uuid4())
            client_ids.append(client_id)

            clients_data.append(
                (
                    client_id,
                    fake.first_name(),
                    fake.last_name(),
                    fake.email(),
                    fake.phone_number(),
                    fake.address(),
                    random.choice(["active", "inactive"]),
                )
            )

        execute_values(cursor, client_insert_query, clients_data)
        print(f"Inserted {start + current_chunk_size} rows into clients...")

    print("Inserted into clients.")
    return client_ids


def insert_products(cursor):
    print("Inserting into products...")

    product_insert_query = """
        INSERT INTO products
            (product_name, product_category, description)
        VALUES %s
        RETURNING product_id
    """

    categories = ["Eggs and Dairy", "Bakery and Bread", "Fruits and Vegetables", "Meat and Seafood", "Snacks and Sweets"]

    products_data = [
        (
            fake.word(),
            random.choice(categories),
            fake.text(),
        )
        for _ in range(PRODUCTS_COUNT)
    ]

    execute_values(cursor, product_insert_query, products_data)

    product_ids = [row[0] for row in cursor.fetchall()]

    print("Inserted into products.")
    return product_ids


def insert_orders(cursor, client_ids, product_ids):
    print("Inserting into orders...")

    order_insert_query = """
        INSERT INTO orders
            (order_date, client_id, product_id)
        VALUES %s
    """

    order_date_start = datetime.now() - timedelta(days=365 * 5)

    for start in range(0, ORDERS_COUNT, CHUNK_SIZE):
        current_chunk_size = min(CHUNK_SIZE, ORDERS_COUNT - start)

        orders_data = [
            (
                order_date_start + timedelta(days=random.randint(0, 365 * 5)),
                random.choice(client_ids),
                random.choice(product_ids),
            )
            for _ in range(current_chunk_size)
        ]

        execute_values(cursor, order_insert_query, orders_data)
        print(f"Inserted {start + current_chunk_size} rows into orders...")

    print("Inserted into orders.")


def main():
    connection = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        dbname=DATABASE,
        port=PORT,
    )

    try:
        with connection:
            with connection.cursor() as cursor:
                client_ids = insert_clients(cursor)
                product_ids = insert_products(cursor)
                insert_orders(cursor, client_ids, product_ids)

    finally:
        connection.close()


if __name__ == "__main__":
    main()
