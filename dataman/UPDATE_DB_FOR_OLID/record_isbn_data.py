"""
Sort a list of ISBNs, storing valid responses and storing the ISBN of invalid responses for later work.

rate limit maybe 2 seconds per ISBN

All files need their locations fixed. This script was used as a one off here, it can be used elsewhere
but shouldn't be moved.
"""
import time
import pickle
import requests
import json

URL = "https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"

isbn_picklefile = "isbns.pickle"
failed_isbn_filename = "isbn_failed.pickle"
all_json_filename = "isbn_response_data.json"

all_json = {}
failed_isbns = []

with open(isbn_picklefile) as f:
    isbns = pickle.load(f)

# shorter testing list with failure
#isbns = [isbns[0], isbns[1], 'dumpp']


for isbn in isbns:
    r = requests.get(URL.format(isbn=isbn))
    if(r.status_code == 200):
        if r.json():
            print "isbn worked: {}".format(isbn)
            all_json.update(r.json())
        else:
            print "unknown isbn"
            failed_isbns.append(isbn)
    else:
        print "request failed"
        failed_isbns.append(isbn)
    time.sleep(.2)

print type(all_json)
print all_json
print all_json.keys()

print failed_isbns

with open(all_json_filename, 'w') as f:
    json.dump(all_json, f)

with open(failed_isbn_filename, 'w') as f:
    pickle.dump(failed_isbns, f)


