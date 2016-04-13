// 1. LIBRARIES
// - - - - - - - - - - - - - - -

var gulp = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var minifycss = require('gulp-minify-css');
var rename = require('gulp-rename');
var watch = require('gulp-watch');
var livereload = require('gulp-livereload');
var uglify = require('gulp-uglify');
var rimraf = require('rimraf');

// 2. FILE PATHS
// - - - - - - - - - - - - - - -

var paths = {
    sass: [
        'netbox/static/netbox/css/*.scss',
        'tools/static/tools/css/*.scss',
        'profiles/static/profiles/css/*.scss',
        'comments/static/comments/css/*.scss'
    ],
    js: [
        'netbox/static/netbox/javascript/*.js',
        'tools/static/tools/javascript/*.js',
        'profiles/static/profiles/javascript/*.js',
        'comments/static/comments/javascript/*.js'
    ],
    fonts: [
        'netbox/static/netbox/fonts/*',
    ]
}

// 3. TASKS
// - - - - - - - - - - - - - - -

// Cleans the build directory
gulp.task('clean', function(cb) {
  rimraf('./staticfiles/*', cb);
})

// Copies fonts
gulp.task('fonts', function() {
    return gulp.src(paths.fonts)
    .pipe(gulp.dest('staticfiles/fonts'));
});

// Compiles Sass
gulp.task('sass', function() {
    return gulp.src(paths.sass)
    .pipe(sass())
    .pipe(autoprefixer({browsers: ['last 2 versions', 'ie 10']}))
    .pipe(gulp.dest('.tmp/css'))
    .pipe(rename({suffix: '.min'}))
    .pipe(minifycss())
    .pipe(gulp.dest('staticfiles/css'))
    .pipe(livereload());
});

// Compiles JS
gulp.task('uglify', function() {
  return gulp.src(paths.js)
    //.pipe(uglify().on('error', function(e){
    //    console.log(e);
    // }))
    .pipe(gulp.dest('staticfiles/js'))
    .pipe(livereload());
});

gulp.task('copyjs', function() {
    return gulp.src(paths.js)
    .pipe(gulp.dest('staticfiles/js'))
    .pipe(livereload());
});

gulp.task('watch', function() {
    livereload.listen();
    
    // Watch fonts
    gulp.watch(paths.fonts, ['fonts']);

    // Watch Sass
    gulp.watch(paths.sass, ['sass']);

    // Watch javascript
    gulp.watch(paths.js, ['copyjs']);

    // Watch Django temlates
    gulp.watch('**/templates/*').on('change', livereload.changed);

});

// Builds your entire app once, without starting a server
gulp.task('build', ['fonts', 'sass', 'uglify']);

// Default task: builds your app, starts a server, and recompiles assets when they change
gulp.task('default', ['fonts', 'sass', 'copyjs', 'watch']);
