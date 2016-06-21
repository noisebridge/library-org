""" method for rendering requested books

Main module will build a dictionary from a json string, in this case from a file.
"""


def reorganize_openlibrary_data(k, v):
    """ Prepare openlibrary data to become a book object.

    The k value isn't really used anymore but it is preserved for now.
    """

    def serialize_multi_entry_fields(multi_entry_list, extraction_key="", separator="; "):
        """ Take a list of similar dicts and serialize some contents to a string

        This dict structure is specific to openlibrary.
        The extraction key is specific to the list of dicts being encoded.
        The separator is arbitrary and used for readibility and later parsing.
        """
        # intermediate list which will be joined to produce the encoded string
        result_list = list()

        for dict_item in multi_entry_list:
            result_list.append(dict_item[extraction_key])

        return separator.join(result_list)

    # what is this dict for? possibly intended to make a dict instead of list.
    # see note below where the list is added to session.
    bookdata_dict = dict()

    simpledata_list = list()

    # Try for each ISBN, prefer ISBN13.
    ISBN_acquired = False
    isbn_to_store = ""
    try:
        # try the isbn 13 then the 10
        isbn_to_store = v['identifiers']['isbn_13'][0]
        ISBN_acquired = True
    except KeyError:
        pass

    # get the isbn10 if the isbn13 failed.
    if not ISBN_acquired:
        try:
            # try the isbn 13 then the 10
            isbn_to_store = v['identifiers']['isbn_10'][0]
            ISBN_acquired = True
        except KeyError:
            pass

    # append isbn or empty string.
    simpledata_list.append(isbn_to_store)

    try:
        # just take the first one in the list
        simpledata_list.append(v['identifiers']['openlibrary'][0])
    except KeyError:
        simpledata_list.append("")

    try:
        # just take the first one in the list
        simpledata_list.append(v['identifiers']['lccn'][0])
    except KeyError:
        simpledata_list.append("")

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

    try:
        simpledata_list.append(serialize_multi_entry_fields(v['authors'],'name'))
    except KeyError:
        simpledata_list.append("")

    try:
        simpledata_list.append(serialize_multi_entry_fields(v['subjects'],'name'))
    except KeyError:
        simpledata_list.append("")

    try:
        simpledata_list.append(v["cover"]["medium"])    
    except KeyError:
        simpledata_list.append("")
    try:
        simpledata_list.append(v["ebooks"][0]["preview_url"])    
    except KeyError:
        simpledata_list.append("")

    try:
        simpledata_list.append(v['classifications']['dewey_decimal_class'][0])
    except KeyError:
        simpledata_list.append("")

    # location
    simpledata_list.append("")

    return simpledata_list


if __name__ == "__main__":
    """
    """
    from controller import db, Book
    from sqlalchemy.exc import IntegrityError

    import json

    # import this to build a database
    # no idea why you would want this, but it can be used as a base for manual fixtures or something.
    db.create_all()

    sourcejsonfile = "dataman/UPDATE_DB_FOR_OLID/isbn_response_data_052916_1628.json"

    with open(sourcejsonfile) as f:
        source_data = json.load(f)

    # bookdata_list order: 0. isbn, 1. title, 2. # pages, 3. publish_date, 4. authors.
    # there are more fields but this needs to become a dict
    for k, v in source_data.iteritems():

        bookdata_list = reorganize_openlibrary_data(k, v)

        # convert this to a dict and pass to session that way
        """
        bookdata = Book(bookdata_list[0], 
                        bookdata_list[1], 
                        bookdata_list[2], 
                        bookdata_list[3], 
                        bookdata_list[4], 
                        bookdata_list[5],
                        bookdata_list[6],
                        bookdata_list[7],
                        bookdata_list[8],
                        bookdata_list[9],
                        bookdata_list[10])
        """
        # just use unpack for now
        bookdata = Book(*bookdata_list)

        db.session.add(bookdata)


        try:
            db.session.commit()
        except IntegrityError:
            print("Book failed, already included: {}".format(bookdata_list[1], bookdata_list[0]))
            db.session.rollback()

