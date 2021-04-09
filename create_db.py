from app import db, Vine, Sort, Producer
import os

if  os.path.exists('vines.sqlite'):
    os.remove('vines.sqlite')

db.create_all()

koblevo = Producer(name='Коблево')
massandra = Producer(name='Массандра')
vardiani = Producer(name='Вардиани')
for item in koblevo, massandra, vardiani:
    db.session.add(item)

red_dry = Sort(name='красное сухое')
red_semidry = Sort(name='красное полусухое')
white_dry = Sort(name='белое сухое')
red_sweet = Sort(name='красное десертное')
for item in red_dry, red_semidry, white_dry,red_sweet:
    db.session.add(item)

vines = [
    Vine(name='каберне',   price=45.0, producer=koblevo,   sort=red_dry, bestseller=1),
    Vine(name='мерло',     price=50.0, producer=massandra, sort=red_semidry),
    Vine(name='алиготе',   price=40.0, producer=massandra, sort=white_dry, bestseller=1),
    Vine(name='портвейн',  price=65.0, producer=koblevo,   sort=red_sweet),
    Vine(name='хванчкара', price=90.0, producer=vardiani,  sort=red_semidry, bestseller=1),
    Vine(name='кагор',     price=65.0, producer=massandra, sort=red_sweet),
    Vine(name='саперави',  price=70.0, producer=vardiani,  sort=red_dry),
    Vine(name='каберне',   price=50.0, producer=massandra, sort=red_dry),
    Vine(name='шардоне',   price=55.0, producer=koblevo,   sort=white_dry),
]

db.session.add_all(vines)
db.session.commit()