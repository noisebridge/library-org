"""
Filter barcodes by length and move into pickle files.
"""
import sqlite3
import pickle

dbfile = 'barcodes.sqlite.bkp.120815.2336'

conn = sqlite3.connect(dbfile)
c = conn.cursor()
barcodes = c.execute("SELECT * FROM BARCODE").fetchall()
conn.close()

barcode13 = list() 
barcode12 = list() 
barcode10 = list() 
barcode_unexpected = list() 

for barcode_wrap in barcodes:
    if len(barcode_wrap[0]) == 13:
        barcode13.append(barcode_wrap[0])
    elif len(barcode_wrap[0]) == 12:
        barcode12.append(barcode_wrap[0])
    elif len(barcode_wrap[0]) == 10:
        barcode10.append(barcode_wrap[0])
    else:
        barcode_unexpected.append(barcode_wrap[0])

# simple length check, success
print (len(barcodes) == len(barcode13) + len(barcode12) + len(barcode10) + len(barcode_unexpected))
# print len(barcode13), len(barcode12), len(barcode10), len(barcode_unexpected)

print barcode_unexpected

isbn_file = "isbn.pickle"
upc_file = "upc.pickle"
unknowns_file = "unknown_numbers.pickle"

with open(isbn_file, 'w') as f:
    pickle.dump(barcode13+barcode10, f)

with open(upc_file, 'w') as f:
    pickle.dump(barcode12, f)

with open(unknowns_file, 'w') as f:
    pickle.dump(barcode_unexpected, f)

