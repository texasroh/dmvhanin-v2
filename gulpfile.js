const gulp = require('gulp');

const css = () => {
    const postCSS = require('gulp-postcss');
    const sass = require('gulp-sass')(require('node-sass'));
    const minify = require('gulp-csso');
    return gulp.src('assets/scss/styles.scss', { allowEmpty: true })
        .pipe(sass().on('error', sass.logError))
        .pipe(postCSS([require('tailwindcss'), require('autoprefixer')]))
        .pipe(minify())
        .pipe(gulp.dest('static/css'));
};

exports.default = css;