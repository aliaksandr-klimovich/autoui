import cherrypy


base_port = 8080
base_url = 'http://127.0.0.1:' + str(base_port)


class Root(object):
    @cherrypy.expose
    def waiters(self):
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

    @cherrypy.expose
    def table(self):
        return """<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 5px;
}
</style>
<body>

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>IP</th>
            <th>Time</th>
            <th>Started</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>name1</td>
            <td>127.0.0.1</td>
            <td>0 days, 6:37:32</td>
            <td>Thu, 18 Feb 2016 09:05:15</td>
            <td>up</td>
        </tr>
        <tr>
            <td>name2</td>
            <td>127.0.0.2</td>
            <td>0 days, 0:24:59</td>
            <td>Thu, 18 Feb 2016 15:15:26</td>
            <td>down</td>
        </tr>
        <tr>
            <td>name3</td>
            <td>127.0.0.3</td>
            <td>0 days, 7:43:54</td>
            <td>Thu, 18 Feb 2016 07:57:12</td>
            <td>down</td>
        </tr>
        <tr>
            <td>name4</td>
            <td>127.0.0.4</td>
            <td>0 days, 8:18:11</td>
            <td>Thu, 18 Feb 2016 07:15:12</td>
            <td>down</td>
        </tr>
        <tr>
            <td>name5</td>
            <td>127.0.0.5</td>
            <td>0 days, 6:44:37</td>
            <td>Thu, 18 Feb 2016 08:55:45</td>
            <td>down</td>
        </tr>
        <tr>
            <td>name6</td>
            <td>127.0.0.6</td>
            <td>0 days, 8:17:46</td>
            <td>Thu, 18 Feb 2016 07:17:13</td>
            <td>down</td>
        </tr>
    </tbody>
</table>

</body>
</html>"""

    @cherrypy.expose
    def checkbox(self):
        return """<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>

<form action="">
<input type="checkbox" name="vehicle" value="Bike" id="ch-01">I have a bike<br>
<input type="checkbox" name="vehicle" value="Car" id="ch-02">I have a car
</form>

<script>
document.getElementById("ch-01").checked = true;
</script>

</body>
</html>"""

    @cherrypy.expose
    def select(self):
        return """<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>

<select id="s-01">
  <option value="volvo">Volvo</option>
  <option value="saab">Saab</option>
  <option value="mercedes">Mercedes</option>
  <option value="audi">Audi</option>
</select>

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


if __name__ == '__main__':
    cherrypy.quickstart(Root())
