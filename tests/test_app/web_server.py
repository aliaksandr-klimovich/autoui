import cherrypy


base_port = '8080'
base_url = 'http://127.0.0.1:' + base_port


class Root(object):
    @cherrypy.expose
    def page1(self):
        return """<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>

<button id="b-01">Click me</button>
<button id="b-02" style="visibility: hidden">Text</button>

<script>
document.getElementById("b-01").onclick = function(e) {
    setTimeout(function(){
        var e = document.getElementById("b-02");
        var v = e.style.visibility;
        if (v == "hidden") {
            e.style.visibility = "visible";
        } else if (v == "visible" || v == "") {
            e.style.visibility = "hidden";
        }
    }, 2000);
    e.stopPropagation();
};
</script>

</body>
</html>"""


def start_test_web_app():
    cherrypy.config.update({
        'server.socket_port': base_port,
        'log.screen': False,
    })
    cherrypy.tree.mount(Root(), '/', {'/': {'tools.gzip.on': True}})
    cherrypy.engine.start()


def stop_test_web_app():
    cherrypy.engine.stop()
    cherrypy.engine.exit()
