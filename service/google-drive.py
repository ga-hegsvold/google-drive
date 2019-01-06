# https://github.com/nithinmurali/pygsheets/tree/master
import pygsheets
import json
import logging
import os
from flask import Flask, Response

# get env.vars
credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_CONTENT")

# set up logging
log_level = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))
logging.basicConfig(level=log_level, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# write out service config from env var to known file
with open(credentials_path, "wb") as out_file:
    out_file.write(credentials.encode())

# authenticate
#gc = pygsheets.authorize(client_secret='client_secret.json')
gc = pygsheets.authorize(client_secret=credentials_path)


# initialize web service
app = Flask(__name__)


@app.route("/<spreadsheet>/<worksheet>")
def download(spreadsheet, worksheet):

    # open spreadsheet by id
    try:
        sh = gc.open_by_key(spreadsheet)
        logging.info("Using spreadsheet: {}".format(sh))
    except Exception as e:
        logging.error("Spreadsheet '{}' not found. {}".format(spreadsheet, e))
        return Response("Spreadsheet not found!")

    # open worksheet by title.
    try:
        wks = sh.worksheet_by_title(worksheet)
        logging.info("Using worksheet: {}".format(wks))
    except Exception as e:
        logging.error("Worksheet '{}' not found. {}".format(worksheet, e))
        return Response("Worksheet not found!")

    # get all cells and format as JSON
    cells = wks.get_all_values()
    json_cells = json.dumps(cells)
    json_rows = json.loads(json_cells)

    # isolate worksheet headers
    header = json_rows[0]

    # transform worksheet from list of rows into list of JSON entities
    result = []
    # skip headers; they are already isolated
    for row in json_rows[1:]:
        item = dict()
        for header_index in range(len(header)):
            item[header[header_index]] = row[header_index]

        result.append(item)

    # return worksheet as JSON
    return Response(json.dumps(result), mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)  # port must match the port exposed in the Dockerfile
