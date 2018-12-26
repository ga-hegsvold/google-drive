# google-drive-service

A python microservice to fetch data from google drive spreadsheets as JSON entities.

**Note: Expects headers in row 1 which will be used as keys for the resulting JSON entities.**

Transforms spreadsheet content on the following form:

.| A | B
:---:|:---:|:---:
1|Header1|Header2
2|Value1|Value2
3|Value3|Value4

into the following JSON entities:
```
[
    {
        "Header1": "Value1",
        "Header2": "Value2"
    },
    {
        "Header1": "Value3",
        "Header2": "Value4"
    }
]
```

## Environment variables
`CLIENT_CREDENTIALS_FILE` - path to credentials file.

`CLIENT_CREDENTIALS_CONTENT` - JSON representation of client credentials to be put into `CLIENT_CREDENTIALS_FILE`.

### Optional

`LOG_LEVEL` the level of logging _(default: INFO)_ (Ref: https://docs.python.org/3/howto/logging.html#logging-levels)


## Docker

Image: https://hub.docker.com/r/gamh/google-drive


## Endpoints

The service is running on port 5000 and accepts connections to the following
endpoint:

    GET /<spreadsheet_id>/<worksheet_title>

`spreadsheet_id` is the id of the google spreadsheet.

`spreadsheet_title` is the title of the google worksheet.

## Example Sesam System Config
```
{
  "_id": "google-drive-system-id",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "CLIENT_CREDENTIALS_FILE": "client_secrets.json",
      "CLIENT_CREDENTIALS_CONTENT": "$SECRET(google-drive-credential-content)" 
    },
    "image": "gamh/google-drive:latest",
    "port": 5000
  }
}
```

## Example Sesam Pipe Config
```
{
  "_id": "pipe-id",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "google-drive-system-id",
    "url": "/<spreadsheet_id>/<worksheet_title>"
  }
}
```

