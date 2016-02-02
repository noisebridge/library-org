

Flask Template Project:

This is a subproject with three objectives:

1. Write a dummy sqlalchemy model in sqlite, with option to covert to postgres
2. Write a template with pagination and iteration over a sqlalchemy model
3. Get sqlalchemy model feeding into a template




Reflections after both quick starts:

1. We need to generate a data structure that is iterated over and that must be reflected in routes and views.
    1. Example: We have mywebapp.com/books/1 and that gives the first page of say 20 items.
    2. This would probably redirect mywebapp.com/books to mywebapp.com/books/1
    3. Triggering the template would request the data, which would fire a query on the Books model or something.
        1. `books = Book.query.all() # ripped from flask-sqlalchemy documentation`
        2. `search = Book.query.filter_by(title='exactname?').first()`
        3. This seems to follow the syntax of SQLAlchemy, so those docs would give us a true search filter.
    4. So the model is a class that should be in the global space in our current controller.
        1. Therefore it should be accessible in the templates.
