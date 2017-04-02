''' A script to get ISBN based on UPC via Amazon's Product API


### Instructions
- pip install python-amazon-simple-product-api
- save data file to the same directory
- edit FILENAME and TYPE constant
- run and hopefully profit

'''

#!/usr/bin/env python

import re

from amazon.api import AmazonAPI

AMAZON_ACCESS_KEY = r'AKIAJOMM7FUFCIVQ4NBQ'
AMAZON_SECRET_KEY = r'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'
AMAZON_ASSOC_TAG = r'hacktheplan08-20'
FILENAME = 'upc.pickle'
TYPE='UPC'


def process_pickle_list(raw_text):
    raw_list = raw_text.split('\n')
    processed_list = []
    for line in raw_list:
        digits = re.sub('\D', '', line)
        if len(line) < 10:  # Not sure about the length of other control numbers..
            continue
        processed_list.append(digits)
    return processed_list


def retrieve_amazon_data(id='00000000000', type=TYPE):
    amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)
    try:
        product = amazon.lookup(ItemId=id, IdType=type, SearchIndex='Books')
    except:
        return None

    try:
        return product.isbn
    except AttributeError:  # So probably not a book then?
        return None


if __name__ == '__main__':
    success_isbns = []
    failed_controlnums = []

    file_content = open(FILENAME).read()
    controlnums = process_pickle_list(file_content)
    for controlnum in controlnums:
        ean = retrieve_amazon_data(controlnum)
        if ean == None:
            failed_controlnums.append(controlnum)
            continue
        success_isbns.append(ean)

    print '====== Successful ISBN Responses ======'
    for entry in success_isbns:
        print entry

    print '====== Failed Control Numbers ======'
    for entry in failed_controlnums:
        print entry
