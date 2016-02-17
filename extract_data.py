
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


    # simpledata_list order: 0. isbn, 1. title, 2. # pages, 3. publish_date, 4. authors.
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
            print simpledata_list[7]
        except:
            simpledata_list.append("")
            print "preview fail"


        # this simpledata_list obviously needs to be a dict,
        # it wasn't originally clear if this code would
        # still exist after its first use.
        # this still may be true so I have not changed it yet.
        bookdata = Book(simpledata_list[0], 
                        simpledata_list[1], 
                        simpledata_list[2], 
                        simpledata_list[3], 
                        simpledata_list[4], 
                        simpledata_list[5],
                        simpledata_list[6],
                        simpledata_list[7])

        db.session.add(bookdata)

        try:
            db.session.commit()
        except IntegrityError:
        #except sqlalchemy.exc.IntegrityError:
            print("Book failed, already included: {}".format(simpledata_list[1], simpledata_list[0]))
            db.session.rollback()
            # this is a crappy exception. i need to handly exactly the ON UNIQUE failure condition
            pass

