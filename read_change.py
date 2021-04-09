from app import db, Vine, Sort, Producer

def show_all_vines():
    for vine in Vine.query.all():
        print(vine.id, vine, vine.producer, vine.price, vine.sort)

def show_all_producers():
    for producer in Producer.query.all():
        print(producer)
        for vine in producer.vines:
            print('\t', vine, vine.sort)

if __name__ == '__main__':
    show_all_vines()
    print('-------------')
    #show_all_producers()
    vine = Vine.query.get(int(input('id: ')))
    print(f'вы выбрали {vine} {vine.producer}')
    newname = input('новое название: ')
    vine.name = newname
    db.session.commit()