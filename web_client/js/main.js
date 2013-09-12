var js_dir = '/js/',
    html_dir = '/html',
    cgi = "/cgi-bin/bmstu-fcgi.pl";

window.configuration = {
    content: '',
    containers: {}
};

window.onload = function() {
    prepare_containers();
    Menu.build();
    updatePage();
}

function prepare_containers() {
    var a = window.configuration.containers;
    a.content = $("div#content_layout");
    a.menu = $("div#menu_layout");
    a.header = $("div#header_layout");
    a.footer = $("div#footer_layout");
}

function updatePage(force_update) {
    var act = 'main';
    if (window.location.hash != "") 
        act = window.location.hash.replace(/^#(.+)$/, "$1");
    if (!Data[act]) {
        redirectPage('#main');
        return;
    } 
    if (act != window.configuration.content || force_update) {
        // Remove old content

    }
}

function build(act) {

}

function redirectPage(url){
    newUrlParts = url.split("#");
    currentUrlParts = window.location.href.split("#");
    window.location.href = url; 
    if(newUrlParts[0] == currentUrlParts[0]) {
        console.log("changing");
        window.location.reload(true);
    } else {
        updatePage();
    }
}
