import os
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, get_sales_by_publisher, Publisher, Shop, Book, Stock, Sale

password = os.getenv('DB_PASSWORD')

DSN = f'postgresql://postgres:{password}@localhost:5432/my_data_base'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Чтение данных из JSON-файла
with open('tests_data.json', 'r') as fd:
    data = json.load(fd)


# Обработка записей и добавление в БД
for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }.get(record.get('model'))

    instance = model(id=record.get('pk'), **record.get('fields'))
    session.add(instance)
    session.commit()


# Запрос к базе данных
sales_by_name = get_sales_by_publisher(session, "Pearson")
for sale in sales_by_name:
    print(f"{sale.book_title:<20} | {sale.shop_name:<10} | {sale.purchase_price:<4} | {sale.purchase_date.strftime('%d-%m-%Y')}")


session.close()

