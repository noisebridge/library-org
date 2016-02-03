"""
A data fixture

"""
from controller import db, Book
from sqlalchemy.exc import IntegrityError

# import this to build a database
# no idea why you would want this, but it can be used as a base for manual fixtures or something.
db.create_all()

if __name__ == "__main__":
    """
    """

    # obvious pattern, populate a list of book objects from a dict or something and iterate the try/except below
    somedata = Book('MYISBN1', 'my title is here', 'robbins trent', '1000', '500')
    somedata2 = Book('MYISBN2', 'alchemical surprises', 'root enoch', '1000', '500')

    db.session.add(somedata)
    db.session.add(somedata2)

    try:
        db.session.commit()
    except IntegrityError:
    #except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        # this is a crappy exception. i need to handly exactly the ON UNIQUE failure condition
        pass

    # query
    books = Book.query.all()
    print "all the books: {}".format(books)
    for book in books:
        print "onebook: {}, isbn:{}".format(book, book.isbn)

    print "type: {}".format(type(books))

    # filter
    filter_the_data = Book.query.filter_by(authors='robbins trent').first()
    print "books by trent robbins only: {}".format(filter_the_data)

    # see SQLAlchemy docs for more filters?
