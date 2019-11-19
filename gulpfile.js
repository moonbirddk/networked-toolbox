// 1. LIBRARIES
// - - - - - - - - - - - - - - -
const { watch, task, series, parallel, src, dest } = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
let cleanCSS = require('gulp-clean-css');
var sourcemaps = require('gulp-sourcemaps');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
var pipeline = require('readable-stream').pipeline;

const path = require('path');
const svgmin = require('gulp-svgmin');
const svgstore = require('gulp-svgstore');
const cheerio = require('gulp-cheerio');


// 2. FILE PATHS
// - - - - - - - - - - - - - - -

var paths = {
    sass: [
        'netbox/static/netbox/css/base.scss',
        'tools/static/tools/css/*.scss',
        'profiles/static/profiles/css/*.scss',
        'search/static/search/css/*.scss',
        'comments/static/comments/css/*.scss',
        'activities/static/activities/css/*.scss'
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

// Copies fonts
function fonts() {
    return src(paths.fonts)
        .pipe(dest('staticfiles/fonts'));
}

function iconsprite() {
    return src(paths.icons[0]+".svg")
        .pipe(cheerio({
            run: function ($) {
                $('g[fill]').removeAttr('fill');
            },
            parserOptions: { xmlMode: true }
        }))
        .pipe(svgmin(function getOptions (file) {
            var prefix = path.basename(file.relative, path.extname(file.relative));
            return {
                plugins: [{
                    cleanupIDs: {
                        prefix: prefix + '-',
                        minify: true
                    }
                },{
                    removeXMLProcIns: true
                }, {
                    removeComments: true
                }, {
                    removeDoctype: true
                }, {
                    collapseGroups: true
                }, {
                    moveGroupAttrsToElems: false
                },{
                    removeAttrs: false
                },{
                    removeViewBox: false
                }]
            }
        }))
        .pipe(svgstore({inlineSvg: false}))
        .pipe(dest('staticfiles/icons'))
}

// exports.iconsprite = parallel(iconsprite);


// Copies icons
function icons(){
    return src(paths.icons)
        .pipe(dest('staticfiles/icons'));
}

// Compiles Sass
function css() {
    return src(paths.sass)
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(autoprefixer())
        .pipe(sourcemaps.write())
        .pipe(dest('.tmp/css'))
        .pipe(rename({suffix: '.min'}))
        .pipe(cleanCSS())
        .pipe(dest('staticfiles/css'))
}

// Compiles JS
function javascript() {
    return pipeline(
        src(paths.js),
        uglify(),
        dest('staticfiles/js')
    )
}

function copyjs() {
    return src(paths.js)
        .pipe(dest('staticfiles/js'))
}

function watchfiles() {
    watch(paths.fonts, fonts);
    watch(paths.sassWatch, css);
    watch(paths.js, copyjs);
    watch(paths.icons, iconsprite)
}


exports.watchfiles = series(parallel(fonts,css,copyjs,iconsprite),watchfiles);
exports.build = parallel(fonts, icons, css, javascript, iconsprite);
exports.default = series(parallel(fonts, css, copyjs, iconsprite), watchfiles);