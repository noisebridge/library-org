
## TODO:
Looks like there isn't any default css minifier. Add one! See sage/roots gulpfile.

## Status:
Bower has been installed, gulp has been installed.  Dependencies are now kept in source control.
In order to unpack this project in a new space:
    1. install npm, gulp, bower.
    2. gulp has dependencies in gulpfile.js, bower has dependencies in bower.json.
    3. Put your assets in the src folder.
    4. node_modules, dist (compiled destination of src files), and bower_components are not kept under source control. These can be rebuilt by installing each. dist is built by running 'gulp'

## Notes:
This git repository is very conservative, only ignoring the following: node_modules.
The purpose of this is to allow particular projects 
A bower init has already been completed. This may need revisited.

There are options in gulpfule.js to make the bower command install or update.
THIS NEEDS TO BE BROKEN INTO TWO COMMAND BECAUSE BOWER PACKAGES WILL BE IN .gitignore!!

I have added bower dependencies to satisfy the needs of pinax-bootstrap.
These dependencies need to be wired into gulp and subsequently into whatever base.html or site_base.html is used by the web app.
