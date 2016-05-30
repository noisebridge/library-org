"""
One off to pull all the ISBNs from a sqlite DB and pickle them as a list of strings.

This won't be used again as we are moving to OLIDs.

Althought we can just alter this script to grab OLIDs to regenerate the data again.

"""

import sqlite3


sqlitedb_filename = "books.20160529_030001.sqlite"


conn = sqlite3.connect(sqlitedb_filename)

c = conn.cursor()

get_isbns_statement = "SELECT isbn FROM book"

isbns = c.execute(get_isbns_statement)

isbn_list = list()
for isbn in isbns:
    isbn_list.append(isbn[0])


import pickle
list_picklefile = "isbns.pickle"

with open(list_picklefile, 'w') as f:
    pickle.dump(isbn_list, f)

