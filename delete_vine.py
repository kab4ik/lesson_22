from app import Vine, db
from read_change import show_all_vines


if __name__ == '__main__':
    show_all_vines()
    id_to_del = int(input('id вина к удалению: '))
    vine_to_del = Vine.query.get(id_to_del)
    db.session.delete(vine_to_del)
    db.session.commit()