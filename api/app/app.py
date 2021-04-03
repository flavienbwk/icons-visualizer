from flask import Flask, Response, send_from_directory, abort
import magic

# Workaround for werkzeug issue (https://github.com/jarus/flask-testing/issues/143#issuecomment-750885274)
try:
    from flask_restplus import Resource, Api
except ImportError:
    import werkzeug
    werkzeug.cached_property = werkzeug.utils.cached_property
    from flask_restplus import Resource, Api

import config
from utils.Icons import Icons
from utils.ApiResponse import ApiResponse


app = Flask(__name__)
api = Api(app, title=config.FLASK_SERVER_NAME, description=config.FLASK_SERVER_DESCRIPTION)

icons = Icons()
icons.updateImages()

@api.route('/api')
class Home(Resource):
    def get(self):
        apiResponse = ApiResponse()
        apiResponse.setAll(False, "Everything's up and running", {
            "nb_images": len(icons.getImagesData())
        })
        return apiResponse.getResponse()


@api.route('/api/icon/<string:icon_hash>')
class Icon(Resource):
    def get(self, icon_hash):
        apiResponse = ApiResponse()
        icon = icons.getImageData(icon_hash)
        if (icon):
            icon.update({"request": icon_hash})
            apiResponse.setAll(False, "Image found", icon)
        else:
            apiResponse.setAll(True, "Image not found", {"request": icon_hash})
        return apiResponse.getResponse()


@api.route('/api/icons', defaults={'query': None, 'limit': 50})
@api.route('/api/icons/<string:query>/<int:limit>')
class Icon(Resource):
    def get(self, query, limit):
        apiResponse = ApiResponse()
        icons_found = icons.searchImages(query, limit)
        apiResponse.setError(False if (len(icons_found)) else True)
        apiResponse.setMessage(str(len(icons_found)) + " images found for your query" if (len(icons_found)) else "No image found for that query")
        apiResponse.setDetails(icons_found)
        return apiResponse.getResponse()


@app.route('/api/file/<string:icon_hash>')
def get_image(icon_hash):
    icon = icons.getImageData(icon_hash)
    if (icon):
        mime_type = magic.from_file(icon["path"], mime=True)
        return send_from_directory(
            icon["parent"],
            icon["filename"],
            mimetype=mime_type if icon["extension"] != "svg" else "image/svg+xml",
            as_attachment=True
        )
    abort(404)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
