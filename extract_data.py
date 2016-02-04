
from controller import db, Book
from sqlalchemy.exc import IntegrityError

# import this to build a database
# no idea why you would want this, but it can be used as a base for manual fixtures or something.
db.create_all()

if __name__ == "__main__":
    """
    """

    import json

    sourcejsonfile = "dataman/isbn_response_data.020316.2343.json"

    with open(sourcejsonfile) as f:
        source_data = json.load(f)


    for k, v in source_data.iteritems():
        simpledata_list = list()
        simpledata_list.append(k[5:])
        try:
            simpledata_list.append(v['title'])
        except KeyError:
            simpledata_list.append("")
        try:
            simpledata_list.append(v['number_of_pages'])
        except KeyError:
            simpledata_list.append("")
        try:
            simpledata_list.append(v['publish_date'])
        except KeyError:
            simpledata_list.append("")
        author_list = ""
        try:
            for author in v['authors']:
                author_list += author['name']
                author_list += " "
        except KeyError:
            pass
        simpledata_list.append(author_list)
        bookdata = Book(simpledata_list[0], simpledata_list[1], simpledata_list[2], simpledata_list[3], simpledata_list[4])

        db.session.add(bookdata)

        try:
            db.session.commit()
        except IntegrityError:
        #except sqlalchemy.exc.IntegrityError:
            print("Book failed, already included: {}".format(simpledata_list[1], simpledata_list[0]))
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


""" Bulk extract our fields from json and put them into the SQLAlchemy model.


"""
