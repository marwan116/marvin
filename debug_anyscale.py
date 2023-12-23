import os
from dotenv import load_dotenv
from openai import OpenAI

# params = {
#     "messages": [
#         {
#             "content": (
#                 "The user will provide context as text that you need to parse into a"
#                 " structured form. To validate your response, you must call the"
#                 " `FormatResponse` function. Use the provided text to extract or infer"
#                 " any parameters needed by `FormatResponse`, including any missing"
#                 " data."
#             ),
#             "role": "system",
#         },
#         {"content": "The text to parse: The Big Apple", "role": "user"},
#     ],
#     "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
#     "temperature": 0.2,
#     "tools": [
#         {
#             "type": "function",
#             "function": {
#                 "name": "FormatResponse",
#                 "description": "Formats the response.",
#                 "parameters": {
#                     "description": "Formats the response.",
#                     "properties": {
#                         "data": {
#                             "type": "object",
#                             "allOf": [
#                                 {
#                                     "type": "object",
#                                     "Location": {
#                                         "description": "Location model.",
#                                         "properties": {
#                                             "city": {
#                                                 "description": (
#                                                     "The inferred official name of a"
#                                                     " real city in the United States"
#                                                 ),
#                                                 "title": "City",
#                                                 "type": "string",
#                                             },
#                                             "state_abbreviation": {
#                                                 "description": (
#                                                     "The two-letter state abbreviation"
#                                                 ),
#                                                 "title": "State Abbreviation",
#                                                 "type": "string",
#                                             },
#                                         },
#                                         "required": ["city", "state_abbreviation"],
#                                         "title": "Location",
#                                         "type": "object",
#                                     }
#                                 }
#                             ],
#                             "description": "The data to format.",
#                         }
#                     },
#                     "required": ["data"],
#                     "type": "object",
#                 },
#             },
#         }
#     ],
#     "tool_choice": {"type": "function", "function": {"name": "FormatResponse"}},
# }

# params = {
#     "messages": [
#         {
#             "content": (
#                 "The user will provide context as text that you need to parse into a"
#                 " structured form. To validate your response, you must call the"
#                 " `FormatResponse` function. Use the provided text to extract or infer"
#                 " any parameters needed by `FormatResponse`, including any missing"
#                 " data."
#             ),
#             "role": "system",
#         },
#         {"content": "The text to parse: The Big Apple", "role": "user"},
#     ],
#     "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
#     "temperature": 0.2,
#     "tools": [
#         {
#             "type": "function",
#             "function": {
#                 "name": "FormatResponse",
#                 "description": "Formats the response.",
#                 "parameters": {
#                     "$defs": {
#                         "type": "object",
#                         "Location": {
#                             "description": "Location model.",
#                             "properties": {
#                                 "city": {
#                                     "description": (
#                                         "The inferred official name of a real city in"
#                                         " the United States"
#                                     ),
#                                     "title": "City",
#                                     "type": "string",
#                                 },
#                                 "state_abbreviation": {
#                                     "description": "The two-letter state abbreviation",
#                                     "title": "State Abbreviation",
#                                     "type": "string",
#                                 },
#                             },
#                             "required": ["city", "state_abbreviation"],
#                             "title": "Location",
#                             "type": "object",
#                         },
#                     },
#                     "description": "Formats the response.",
#                     "properties": {
#                         "data": {
#                             "allOf": [
#                                 {
#                                     "type": "object",
#                                     "$ref": (
#                                         "#/tools/0/function/parameters/$defs/Location"
#                                     ),
#                                 }
#                             ],
#                             "description": "The data to format.",
#                         }
#                     },
#                     "required": ["data"],
#                     "type": "object",
#                 },
#             },
#         }
#     ],
#     "tool_choice": {"type": "function", "function": {"name": "FormatResponse"}},
# }

# params = {
#     "messages": [
#         {
#             "role": "system",
#             "content": (
#                 "The user will provide text that you need to parse into a\nstructured"
#                 " form .\nTo validate your response, you must call"
#                 " the\n`FormatResponse` function.\nUse the provided text and context to"
#                 " extract, deduce, or infer\nany parameters needed by `FormatResponse`,"
#                 " including any missing\ndata.\n\nYou have been provided the following"
#                 " context to perform your task:\n    - The current time is 2023-12-22"
#                 " 20:34:50.635612+00:00."
#             ),
#         },
#         {"role": "user", "content": "The text to parse: The Big Apple"},
#     ],
#     "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
#     "temperature": 0.8,
#     "tools": [
#         {
#             "type": "function",
#             "function": {
#                 "name": "FormatResponse",
#                 "description": "",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "city": {"title": "City", "type": "string"},
#                         "state_abbreviation": {
#                             "title": "State Abbreviation",
#                             "description": "The two-letter state abbreviation",
#                             "type": "string",
#                         },
#                     },
#                     "required": ["city", "state_abbreviation"],
#                 },
#             },
#         }
#     ],
#     "tool_choice": "auto",
# }

import jsonref
import json

load_dotenv()

client = OpenAI(
    api_key=os.environ["ANYSCALE_API_KEY"],
    base_url="https://api.endpoints.anyscale.com/v1",
)

# params_deref = jsonref.loads(json.dumps(params))

params_deref = {
    "messages": [
        {
            "content": (
                "The user will provide context as text that you need to parse into a"
                " structured form. To validate your response, you must call the"
                " `FormatResponse` function. Use the provided text to extract or infer"
                " any parameters needed by `FormatResponse`, including any missing"
                " data."
            ),
            "role": "system",
        },
        {"content": "The text to parse: The Big Apple", "role": "user"},
    ],
    "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "temperature": 0.2,
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "FormatResponse",
                "description": "Formats the response.",
                "parameters": {
                    "description": "Formats the response.",
                    "properties": {
                        "data": {
                            "allOf": [
                                {
                                    "description": "Location model.",
                                    "properties": {
                                        "city": {
                                            "description": (
                                                "The inferred official name of a real"
                                                " city in the United States"
                                            ),
                                            "title": "City",
                                            "type": "string",
                                        },
                                        "state_abbreviation": {
                                            "description": (
                                                "The two-letter state abbreviation"
                                            ),
                                            "title": "State Abbreviation",
                                            "type": "string",
                                        },
                                    },
                                    "required": ["city", "state_abbreviation"],
                                    "title": "Location",
                                    "type": "object",
                                }
                            ],
                            "description": "The data to format.",
                            "type": "object",
                        }
                    },
                    "required": ["data"],
                    "type": "object",
                },
            },
        }
    ],
    "tool_choice": {"type": "function", "function": {"name": "FormatResponse"}},
}


out = client.chat.completions.create(**params_deref)

print(out)
