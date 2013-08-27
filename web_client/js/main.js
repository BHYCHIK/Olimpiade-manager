var js_dir = '/js/',
    html_dir = '/html';
var source_reader = '/cgi-bin/read_sources.pl';

var actions = {
    __container: 'content_layout',
    register_person: {
        source: 'registration.htm',
        handler: Registration.show,
        data: undefined
    }
};

var menu_container = {
    __container: 'menu_layout',
    login_form: {
        source: 'user_box.htm',
        data: undefined
    }
};

window.action = actions.register_person;

window.onload = function() {
    // Check for the various File API support.
    if (window.File && window.FileReader && window.FileList && window.Blob) {
        // All the File APIs are supported.
        build_content();
        build_menu();
    } else {
        alert('The File APIs are not fully supported in your browser.');
    }
}

function build_content() {

}

function build_menu() {
    var url = source_reader + "?";
    var i = 0;
    for (var form in menu_container) if (!/^__/.test(form)) {
        if (!menu_container[form].data) {
            i++; url += form + "=" + menu_container[form].source + "&";
        }
    }
    if (i) {
        $.getJSON(url.replace(/&$/, ""), function (data) {
            for (var key in data) {
                menu_container[key].data = data[key];
            }
        });
    }
}
