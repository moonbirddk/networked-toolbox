// 1. LIBRARIES
// - - - - - - - - - - - - - - -

var gulp = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var minifycss = require('gulp-minify-css');
var sourcemaps = require('gulp-sourcemaps');
var rename = require('gulp-rename');
var watch = require('gulp-watch');
var livereload = require('gulp-livereload');
var uglify = require('gulp-uglify');
var rimraf = require('rimraf');
var browserSync = require('browser-sync').create();
var reload = browserSync.reload;
var url = 'http://localhost:8000';
// 2. FILE PATHS
// - - - - - - - - - - - - - - -

var paths = {
    sass: [
        'admin_tools/css/theming.css',
        'netbox/static/netbox/css/base.scss',
        'tools/static/tools/css/*.scss',
        'profiles/static/profiles/css/*.scss',
        'search/static/search/css/*.scss',
        'comments/static/comments/css/*.scss',
        'activities/static/activities/css/*.scss',
        ''
    ],
    sassWatch: [
        'netbox/static/netbox/css/*.scss'
    ],
    js: [
        'netbox/static/netbox/javascript/*.js',
        'tools/static/tools/javascript/*.js',
        'profiles/static/profiles/javascript/*.js',
        'comments/static/comments/javascript/*.js'
    ],
    fonts: [
        'netbox/static/netbox/fonts/*',
    ],
    icons: [
        'netbox/static/netbox/icons/*',
    ]
}

paths.sassWatch = paths.sassWatch.concat(paths.sass);

console.log(paths.sassWatch);

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

// Copies icons
gulp.task('icons', function() {
    return gulp.src(paths.icons)
    .pipe(gulp.dest('staticfiles/icons'));
});

// Compiles Sass
gulp.task('sass', function() {
    return gulp.src(paths.sass)
    .pipe(sourcemaps.init())
    .pipe(sass())
    .pipe(autoprefixer({browsers: ['last 2 versions', 'ie 10']}))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('.tmp/css'))
    .pipe(rename({suffix: '.min'}))
    .pipe(minifycss())
    .pipe(gulp.dest('staticfiles/css'))
    // .pipe(livereload());
    .pipe(reload({
        stream: true
    }))
});

// Compiles JS
gulp.task('uglify', function() {
  return gulp.src(paths.js)
    .pipe(uglify().on('error', function(e){
       console.log(e);
    }))
    .pipe(gulp.dest('staticfiles/js'))
    // .pipe(livereload());
});

gulp.task('copyjs', function() {
    return gulp.src(paths.js)
    .pipe(gulp.dest('staticfiles/js'))
    // .pipe(livereload());
});

gulp.task('watch', function() {
    livereload.listen();

    // Watch fonts
    gulp.watch(paths.fonts, ['fonts']);

    // Watch Sass
    gulp.watch(paths.sassWatch, ['sass']);

    // Watch javascript
    gulp.watch(paths.js, ['copyjs']);

    // Watch Django temlates
    gulp.watch('**/templates/*').on('change', livereload.changed);

});

gulp.task('default', function() {
    browserSync.init({
        proxy: url,
        open: false,
        notify: false,
        ghostMode: {
            clicks: true,
            scroll: true,
            forms: {
                submit: true,
                inputs: true,
                toggles: true
            }
        }
    });

    // Watch fonts
    gulp.watch(paths.fonts, ['fonts']);
    // Watch fonts
    gulp.watch(paths.icons, ['icons']);

    // Watch Sass
    gulp.watch(paths.sassWatch, ['sass']);

    // Watch javascript
    gulp.watch(paths.js, ['copyjs']);

    // Watch Django temlates
    // gulp.watch(['**/*.html', '**/*.py']).on('change', reload);
    gulp.watch(['**/*.html']).on('change', reload);

});



// Builds your entire app once, without starting a server
gulp.task('build', ['fonts', 'icons', 'sass', 'uglify']);

// Default task: builds your app, starts a server, and recompiles assets when they change
gulp.task('watch', ['fonts', 'sass', 'copyjs', 'watch']);

