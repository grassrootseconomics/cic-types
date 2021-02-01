"""This module describes the JSON schema for the validation of data of the "person" type in CIC custom data objects
N/B: The regex patters defined herein follow the javascript ECMA 262 format as supported under json-schema for JSON
validation.
For more see: https://json-schema.org/understanding-json-schema/reference/regular_expressions.html#regular-expressions"""
person_json_schema = {
    "type": "object",
    "properties": {
        "date_registered": {
            "type": "number",
            "pattern": "^([0-9]{10})$"
        },
        "gender": {"type": "string"},
        "key": {
            "type": "object",
            "properties": {
                "ethereum": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        },
        "location": {
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "string",
                    "pattern": "^(\-?([0-8]?[0-9](\.\d+)?|90(.[0]+)?)\s?)$"
                },
                "longitude": {
                    "type": "string",
                    "pattern": "^(\-?([1]?[0-7]?[0-9](\.\d+)?|180((.[0]+)?)))$"
                },
                "external": {"type": "object"}
            },
            "required": ["latitude", "longitude"]
        },
        "selling": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "vcard": {
            "type": "string",
            "contentEncoding": "base64",
            "contentMediaType": "text/html"
        }
    },
    "required": ["date_registered", "gender", "key", "location", "selling", "vcard"]
}

vcard_json_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "family": {
            "type": "string",
            "pattern": "^([a-zA-Z]+)$"
        },
        "given": {
            "type": "string",
            "pattern": "^([a-zA-Z]+)$"
        },
        "tel": {
            "type": "string",
            "pattern": "^([+254]?[0-9]{12})$"
        }
    }
}
