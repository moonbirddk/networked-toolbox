// 1. LIBRARIES
// - - - - - - - - - - - - - - -

var gulp = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var minifycss = require('gulp-minify-css');
//var sourcemaps = require('gulp-sourcemaps');
var rename = require('gulp-rename');
//var watch = require('gulp-watch');
//var livereload = require('gulp-livereload');
var uglify = require('gulp-uglify');
var rimraf = require('rimraf');
//var browserSync = require('browser-sync').create();
//var reload = browserSync.reload;
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


// 3. TASKS
// - - - - - - - - - - - - - - -

// Cleans the build directory
function clean() {
    return gulp.src(paths.clean)
        .pipe(rimraf('./staticfiles/*', cb))
  
}

// Copies fonts
function fonts() {
    return gulp.src(paths.fonts)
        .pipe(gulp.dest('staticfiles/fonts'));
}

// Copies icons
function icons(){
    return gulp.src(paths.icons)
        .pipe(gulp.dest('staticfiles/icons'));
}

// Compiles Sass
function sass() {
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
    
}

// Compiles JS
function uglify() {
  return gulp.src(paths.js)
    .pipe(uglify().on('error', function(e){
       console.log(e);
    }))
    .pipe(gulp.dest('staticfiles/js'))
    // .pipe(livereload());
}

function copyjs() {
    return gulp.src(paths.js)
    .pipe(gulp.dest('staticfiles/js'))
    // .pipe(livereload());
}



function watchall() {
    

    // Watch fonts
    gulp.watch(paths.fonts, fonts);

    // Watch Sass
    gulp.watch(paths.sassWatch, sass);

    // Watch javascript
    gulp.watch(paths.js, copyjs);



};

gulp.task('default', gulp.series(function(done) {

    // Watch fonts
    gulp.watch(paths.fonts, fonts);
    // Watch fonts
    gulp.watch(paths.icons, icons);

    // Watch Sass
    gulp.watch(paths.sassWatch, sass);

    // Watch javascript
    gulp.watch(paths.js, copyjs);

    // Watch Django temlates
    // gulp.watch(['**/*.html', '**/*.py']).on('change', reload);
    //gulp.watch(['**/*.html']).on('change', reload);

}));



// Builds your entire app once, without starting a server
gulp.task('build', gulp.parallel(function(done) {
    fonts()
    icons()
    sass()
    uglify()
    done()
} ));

// Default task: builds your app, starts a server, and recompiles assets when they change
//gulp.task('watch', ['fonts', 'sass', 'copyjs', 'watch']);

