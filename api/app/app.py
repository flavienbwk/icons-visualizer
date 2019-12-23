from flask import Flask, request, send_file, abort
from flask_restplus import Api, Resource

import config
from icons import Icons
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
            "nb_images": 0
        })
        return apiResponse.getResponse()

@api.route('/api/icon/<string:icon_filename>')
class Icon(Resource):
    def get(self, icon_filename):
        apiResponse = ApiResponse()
        icon = icons.getImageData(icon_filename)
        if (icon):
            icon.update({"request": icon_filename})
            apiResponse.setAll(False, "Image found", icon)
        else:
            apiResponse.setAll(True, "Image not found", {"request": icon_filename})
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

@app.route('/icon/<string:icon_filename>')
def get_image(icon_filename):
    icon = icons.getImageData(icon_filename)
    if (icon):
        filename = icons.abs_path + "/icons/" + icon_filename
        return send_file(filename, mimetype='image/' + icon["extension"])
    abort(404)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")