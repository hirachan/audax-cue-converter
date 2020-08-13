from typing import Optional

import base64

from rwgps import RideWithGPS
from nihonbashi import Nihonbashi


def convert(event, context):
    route_id = event["pathParameters"]["route_id"]

    query: str = event["queryStringParameters"]
    privacy_code: Optional[str]
    if query:
        privacy_code = query.get("privacy_code", None)
    else:
        privacy_code = None

    rwgps = RideWithGPS()
    cues = rwgps.read(route_id, privacy_code)
    converter = Nihonbashi()
    converter.write(cues, "/tmp/output.xlsx")

    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            # "Content-Type": "application/octet-stream",
        },
        "body": base64.b64encode(open("/tmp/output.xlsx", "rb").read()),
        "isBase64Encoded": True
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
