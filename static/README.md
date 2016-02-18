
## TODO:
Looks like there isn't any default css minifier. Add one! See sage/roots gulpfile.

## Dependencies:
1. NodeJS
2. Bower
3. Gulp

## Instructions
In order to unpack this project in a new space:

1. install NodeJS (on OS X: `brew install node`)
2. npm install -g bower gulp
3. npm install
4. bower install
5. gulp

Put your assets in the src folder.
The directories `node_modules`, `dist` (compiled destination of src files), and `bower_components` are not kept under source control. These can be rebuilt by installing each. `dist` is built by running 'gulp'

## Notes:
This git repository is very conservative, only ignoring the following: node_modules.
The purpose of this is to allow particular projects
A bower init has already been completed. This may need revisited.

There are options in gulpfule.js to make the bower command install or update.
THIS NEEDS TO BE BROKEN INTO TWO COMMAND BECAUSE BOWER PACKAGES WILL BE IN .gitignore!!

I have added bower dependencies to satisfy the needs of pinax-bootstrap.
These dependencies need to be wired into gulp and subsequently into whatever base.html or site_base.html is used by the web app.
