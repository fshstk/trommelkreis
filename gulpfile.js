const { series, src, dest } = require("gulp");

function copy_fonts() {
    const files = [
        "node_modules/@fortawesome/fontawesome-free/webfonts/*",
        "node_modules/ubuntu-fontface/fonts/*",
    ];
    return src(files).pipe(dest("_fonts"));
}

function copy_scripts() {
    const files = [
        "node_modules/jquery/dist/jquery.min.js",
        "node_modules/popper.js/dist/popper.min.js",
        "node_modules/bootstrap/dist/js/bootstrap.min.js",
    ];
    return src(files).pipe(dest("_scripts"));
}

// By default, do nothing:
// (This is called when python manage.py runserver is executed.)
exports.default = (cb) => { cb(); };

// (This is called when python manage.py collectstatic is executed.)
exports.build = series(copy_fonts, copy_scripts);
