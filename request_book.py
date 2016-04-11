""" Request methods for rendering requested ISBNs.
"""
def reorganize_openlibrary_data(k, v):
    """ Prepare openlibrary data to become a book object.
    """
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
    author_string = ""
    try:
        for author in v['authors']:
            author_string += author['name']
            author_string += "; "
        simpledata_list.append(author_string.rstrip(" ;"))
    except KeyError:
        simpledata_list.append("")
    subject_string = ""
    try:
        for subject in v["subjects"]:
            subject_string += subject["name"]
            subject_string += "; "
        simpledata_list.append(subject_string.rstrip(" ;"))
    except:
        simpledata_list.append("")
    try:
        simpledata_list.append(v["cover"]["medium"])
    except:
        simpledata_list.append("")
    try:
        # just take the first preview...
        simpledata_list.append(v["ebooks"][0]["preview_url"])
    except:
        simpledata_list.append("")
    try:
        dewey_string = ""
        for dewey_class in v["classifications"]["dewey_decimal_class"]:
            dewey_string += dewey_class
            dewey_string += "; "
        simpledata_list.append(dewey_string.rstrip(" ;"))
    except:
        simpledata_list.append("")

    return simpledata_list


def reorganize_manual_data(fields):
    data_dict = dict()
    for field in fields:
        data_dict[field.label.text] = field.data

    simpledata_list = list()
    def simpledata_try_append(label, dict=data_dict):
        """ Give field label, returns its data or empty string.

        Implemented to avoid multiple trys and excepts.
        Since the user already formatted the data, no more processing is needed.
        """
        try:
            return dict[label]
        except KeyError:
            return ''
    simpledata_list.append(simpledata_try_append('isbn'))
    simpledata_list.append(simpledata_try_append('title'))
    simpledata_list.append(simpledata_try_append('number_of_pages'))
    simpledata_list.append(simpledata_try_append('publish_date'))
    simpledata_list.append(simpledata_try_append('authors'))
    simpledata_list.append(simpledata_try_append('subjects'))
    simpledata_list.append(simpledata_try_append('cover_url'))
    simpledata_list.append(simpledata_try_append('preview_url'))
    simpledata_list.append(simpledata_try_append('dewey_decimal_class'))

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

    sourcejsonfile = "dataman/isbn_response_data.020316.2343.json"

    with open(sourcejsonfile) as f:
        source_data = json.load(f)

    # bookdata_list order: 0. isbn, 1. title, 2. # pages, 3. publish_date, 4. authors.
    # there are more fields but this needs to become a dict
    for k, v in source_data.iteritems():

        bookdata_list = reorganize_openlibrary_data(k, v)

        # this bookdata_list obviously needs to be a dict,
        # it wasn't originally clear if this code would
        # still exist after its first use.
        # this still may be true so I have not changed it yet.
        bookdata = Book(bookdata_list[0],
                        bookdata_list[1],
                        bookdata_list[2],
                        bookdata_list[3],
                        bookdata_list[4],
                        bookdata_list[5],
                        bookdata_list[6],
                        bookdata_list[7],
                        bookdata_list[8])

        db.session.add(bookdata)

        try:
            db.session.commit()
        except IntegrityError:
        #except sqlalchemy.exc.IntegrityError:
            print("Book failed, already included: {}".format(bookdata_list[1], bookdata_list[0]))
            db.session.rollback()
            # this is a crappy exception. i need to handly exactly the ON UNIQUE failure condition
            pass
