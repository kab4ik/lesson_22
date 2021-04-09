from app import db, Vine, Sort, Producer


print('Производители')
for p in Producer.query.all():
    print(p.id, p)

print('Сорта')
for s in Sort.query.all():
    print(s.id, s)

name = input('название: ')
price = float(input('цена: '))
producer_id = int(input('id производителя: '))
producer = Producer.query.get(producer_id)
sort_id = int(input('id сорта: '))
sort = Sort.query.get(sort_id)

newvine = Vine(name=name, price=price, producer=producer, sort=sort)
db.session.add(newvine)
db.session.commit()
