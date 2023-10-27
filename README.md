### Library Organization Project

This project provides organized data about the contents of a library.


##### Project Status

Alpha released.


##### Getting Started
1. fork and clone this repository
2. [create] (https://virtualenvwrapper.readthedocs.org) and activate a [virtualenv] (https://virtualenv.pypa.io)
3. pip install -r requirements.txt
4. cd [static] (static/README.md) && npm install && gulp
5. cp database/books-sample.sqlite database/books.sqlite
6. python controller.py
7. go to [localhost:5000] (http://localhost:5000) in the browser

##### Docker

Build the Docker image:

    docker build -t library-org .

Run the Docker image:

    docker run \
      -p 5000:5000
      -v /path/to/library.cfg:/app/library.cfg \
      -v /path/to/books.sqlite:/app/database/books.sqlite \
      localhost/library-org:latest

##### Features on-deck:

1. Advanced Search
2. API
3. New Book submit-by-isbn with requests to multiple services. User selects service to pull data from.


### API Options:

Programmable Web lists 49 library APIs:
http://www.programmableweb.com/category/library%2Breference/apis?category=20272%2C20066
librarything seems to be a very good 'tooling' api: http://www.librarything.com/api

### Issues:

Database is currently unique on isbn, we care about being unique on open library id, maybe isbn.
There is a place in control flow, the new book form that still relies on ISBN being unique. This should probably wholesale convert to LCCN and still allow people to enter by isbn for convenience. This adds some complexity as there are a great many isbns for one book.
