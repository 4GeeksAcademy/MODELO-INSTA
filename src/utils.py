from flask import jsonify, url_for, Response

class APIException(Exception):
    """
    Excepción personalizada para devolver errores en formato JSON.
    """
    def __init__(self, message, status_code=400, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}

    def to_dict(self):
        rv = dict(self.payload)
        rv["message"] = self.message
        return rv


def has_no_empty_params(rule):
    """
    Verifica que la regla de ruta no requiera parámetros obligatorios.
    """
    defaults = rule.defaults if rule.defaults else ()
    arguments = rule.arguments if rule.arguments else ()
    return len(defaults) >= len(arguments)


def generate_sitemap(app):
    """
    Genera un listado en HTML de todos los endpoints disponibles,
    excluyendo los de administración.
    """
    links = ["/admin/"]
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    links_html = "".join(f"<li><a href='{link}'>{link}</a></li>" for link in links)

    html = f"""
    <div style="text-align: center;">
        <img style="max-height: 80px"
             src="https://storage.googleapis.com/breathecode/boilerplates/rigo-baby.jpeg" />
        <h1>Rigo welcomes you to your API!!</h1>
        <p>API HOST:
            <script>
                document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');
            </script>
        </p>
        <p>Start working on your project by following the
            <a href="https://start.4geeksacademy.com/starters/flask" target="_blank">Quick Start</a>
        </p>
        <p>Available endpoints:</p>
        <ul style="text-align: left;">{links_html}</ul>
    </div>
    """
    return Response(html, mimetype="text/html")
