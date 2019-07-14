// Include gulp
var gulp = require('gulp'); 

// Include Our Plugins
var jshint = require('gulp-jshint');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var imagemin = require('gulp-imagemin');
var pngquant = require('imagemin-pngquant');
var bower = require('gulp-bower');

// NOTES: Currently directories are referenced multiple times. If this file is used more regularly, the directories need to be more DRY. Move them to variables, see sage/roots gulpfile.js for a sample.

// Bower task
gulp.task('bower', function() {
    //return bower({ cmd: 'update'}); // uncomment to enable 'update mode'
    return bower() // uncomment to enable 'install mode' (pick one, update or install)
    .pipe(gulp.dest('lib/'))
});

// Lint Task
function lint() {
    return gulp.src('src/js/**/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
}
exports.lint = lint;

// Compile Our Sass
function saas() {
    return gulp.src('src/scss/**/*.scss')
        .pipe(sass())
        .pipe(gulp.dest('dist'));
}
exports.saas = saas;

// Concatenate & Minify JS
function scripts() {
    return gulp.src('src/js/**/*.js')
        .pipe(concat('all.js'))
        .pipe(gulp.dest('dist'))
        .pipe(rename('all.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('dist'));
}
exports.scripts = scripts;

// Process Images w/ imagemin
function images() {
    return gulp.src('src/images/**/*')
        .pipe(imagemin({
            progressive: true,
            svgoPlugins: [{removeViewBox: false}],
            use: [pngquant()]
        }))
        .pipe(gulp.dest('dist/images'));
}
exports.images = images;

// Watch Files For Changes
function watch() {
    gulp.watch('src/js/**/*.js', ['lint', 'scripts']);
    gulp.watch('src/scss/**/*.scss', ['sass']);
    gulp.watch('src/images/**/*', ['images']);
}
exports.watch = watch;

// Default Task
// TAR 082615 - Added images, removed watch from default.
const build = gulp.series(lint, saas, scripts, images);
exports.default = build;
