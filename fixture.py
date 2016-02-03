"""
A data fixture

"""
from controller import db, Book

# import this to build a database
# no idea why you would want this, but it can be used as a base for manual fixtures or something.
db.create_all()

if __name__ == "__main__":

    try:
        somedata = Book('MYISBN1', 'my title is here', 'robbins trent', '1000', '500')
    except IntegrityError:
        # this is a crappy exception. i need to handly exactly the ON UNIQUE failure condition
        pass
    try:
        somedata2 = Book('MYISBN2', 'my title is here', 'root enoch', '1000', '500')
    except IntegrityError:
        # this is a crappy exception. i need to handly exactly the ON UNIQUE failure condition
        pass


    db.session.add(somedata)
    db.session.add(somedata2)
    db.session.commit()


    # query
    get_the_data = Book.query.all()
    print "all the books: {}".format(get_the_data)

    # filter
    filter_the_data = Book.query.filter_by(authors='robbins trent').first()
    print "books by trent robbins only: {}".format(filter_the_data)

    # see SQLAlchemy docs for more filters?
