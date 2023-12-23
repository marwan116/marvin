from dotenv import load_dotenv

load_dotenv()

import os
from openai import OpenAI
import json

anyscale_client = OpenAI(
    api_key=os.environ["ANYSCALE_API_KEY"],
    base_url="https://api.endpoints.anyscale.com/v1",
)

openai_client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)


# this works as expected for both anyscale and openai
kwargs = {
    "messages": [
        {"content": "You are a helpful assistant.", "role": "system"},
        {"content": "How is the weather in SF in Fahrenheits?", "role": "user"},
    ],
    "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "temperature": 0,
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Gets the weather.",
                "parameters": {
                    "description": "Gets the weather.",
                    "properties": {
                        "city": {
                            "description": "The city to get the weather for.",
                            "title": "City",
                            "type": "string",
                        },
                        "units": {
                            "description": "The units to get the weather in.",
                            "title": "Units",
                            "type": "string",
                        },
                    },
                    "required": ["city", "units"],
                    "type": "object",
                },
            },
        },
    ],
    "tool_choice": {"type": "function", "function": {"name": "get_weather"}},
}


anyscale_response = anyscale_client.chat.completions.create(**kwargs)
anyscale_args = json.loads(
    anyscale_response.choices[0].message.tool_calls[0].function.arguments
)
assert anyscale_args == {"city": "SF", "units": "Fahrenheit"}

openai_response = openai_client.chat.completions.create(
    **{**kwargs, "model": "gpt-3.5-turbo"}
)
openai_args = json.loads(
    openai_response.choices[0].message.tool_calls[0].function.arguments
)
# openai has a hard time inferring Fahrenheits but not really our issue here
assert openai_args == {
    "city": "San Francisco",
    "units": "imperial",
}

# Now we provide a referenced JSON schema - this fails for anyscale but works for openai
kwargs["tools"] = [
    {
        "$defs": {
            "type": "object",
            "Weather": {
                "description": "Weather model.",
                "properties": {
                    "city": {
                        "description": "The city to get the weather for.",
                        "title": "City",
                        "type": "string",
                    },
                    "units": {
                        "description": "The units to get the weather in.",
                        "title": "Units",
                        "type": "string",
                    },
                },
                "required": ["city", "units"],
                "title": "Weather",
                "type": "object",
            },
        },
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Gets the weather.",
            "parameters": {
                "description": "Gets the weather.",
                "properties": {
                    "data": {
                        "allOf": [
                            {"type": "object", "$ref": "#/tools/0/$defs/Weather"}
                        ],
                        "description": "The data to format.",
                    }
                },
                "required": ["data"],
                "type": "object",
            },
        },
    },
]
# this throws an error for anyscale
failed_anyscale = False
try:
    anyscale_response = anyscale_client.chat.completions.create(**kwargs)
except Exception as e:
    failed_anyscale = True
finally:
    assert failed_anyscale

# while openai works as expected
openai_response = openai_client.chat.completions.create(
    **{**kwargs, "model": "gpt-3.5-turbo"}
)
openai_args = json.loads(
    openai_response.choices[0].message.tool_calls[0].function.arguments
)
assert openai_args == {
    "data": {"city": "San Francisco", "unit": "imperial"}
}, openai_args


# to "fix" the anyscale error we need to add a type: object to function/parameters/data/properties/data/allOf
# this "fix" however will make both anyscale and openai return empty objects
kwargs["tools"] = [
    {
        "$defs": {
            "type": "object",
            "Weather": {
                "description": "Weather model.",
                "properties": {
                    "city": {
                        "description": "The city to get the weather for.",
                        "title": "City",
                        "type": "string",
                    },
                    "units": {
                        "description": "The units to get the weather in.",
                        "title": "Units",
                        "type": "string",
                    },
                },
                "required": ["city", "units"],
                "title": "Weather",
                "type": "object",
            },
        },
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Gets the weather.",
            "parameters": {
                "description": "Gets the weather.",
                "properties": {
                    "data": {
                        "type": "object",  # this is the change
                        "allOf": [
                            {"type": "object", "$ref": "#/tools/0/$defs/Weather"}
                        ],
                        "description": "The data to format.",
                    }
                },
                "required": ["data"],
                "type": "object",
            },
        },
    },
]

anyscale_response = anyscale_client.chat.completions.create(**kwargs)
anyscale_args = json.loads(
    anyscale_response.choices[0].message.tool_calls[0].function.arguments
)
# this is the "fix" but it's not really a fix
assert anyscale_args == {"data": {}}, f"Got this instead {anyscale_args=}"

openai_response = openai_client.chat.completions.create(
    **{**kwargs, "model": "gpt-3.5-turbo"}
)
openai_args = json.loads(
    openai_response.choices[0].message.tool_calls[0].function.arguments
)
# this is the "fix" but it's not really a fix
assert openai_args == {}, openai_args


# Note that openai is robust to "relative" or malformed references
kwargs["tools"] = [
    {
        "$defs": {
            "type": "object",
            "Weather": {
                "description": "Weather model.",
                "properties": {
                    "city": {
                        "description": "The city to get the weather for.",
                        "title": "City",
                        "type": "string",
                    },
                    "units": {
                        "description": "The units to get the weather in.",
                        "title": "Units",
                        "type": "string",
                    },
                },
                "required": ["city", "units"],
                "title": "Weather",
                "type": "object",
            },
        },
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Gets the weather.",
            "parameters": {
                "description": "Gets the weather.",
                "properties": {
                    "data": {
                        "allOf": [
                            {
                                "type": "object",
                                "$ref": "#/$defs/Weather",  # note the change
                            }
                        ],
                        "description": "The data to format.",
                    }
                },
                "required": ["data"],
                "type": "object",
            },
        },
    },
]
# this throws an error for anyscale
failed_anyscale = False
try:
    anyscale_response = anyscale_client.chat.completions.create(**kwargs)
except Exception as e:
    failed_anyscale = True
finally:
    assert failed_anyscale


# while openai works as expected
openai_response = openai_client.chat.completions.create(
    **{**kwargs, "model": "gpt-3.5-turbo"}
)
openai_args = json.loads(
    openai_response.choices[0].message.tool_calls[0].function.arguments
)
assert openai_args == {
    "data": {"city": "San Francisco", "unit": "imperial"}
}, openai_args


# this matters because pydantic's model JSON schema generator will return relative references
from pydantic import BaseModel, Field


class Weather(BaseModel):
    """Weather model."""

    city: str = Field(
        ...,
        description="The city to get the weather for.",
    )
    units: str = Field(
        ...,
        description="The units to get the weather in.",
    )


class WeatherResponse(BaseModel):
    """Weather response model."""

    data: Weather = Field(
        ...,
        description="The data to format.",
    )


pydantic_nested_object_json_schema = WeatherResponse.model_json_schema()

kwargs = {
    "messages": [
        {"content": "You are a helpful assistant.", "role": "system"},
        {"content": "How is the weather in SF in Fahrenheits?", "role": "user"},
    ],
    "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "temperature": 0.2,
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Gets the weather.",
                "parameters": {
                    "description": "Gets the weather.",
                    "properties": {
                        f"return": pydantic_nested_object_json_schema,
                    },
                    "required": ["return"],
                    "type": "object",
                },
            },
        },
    ],
    "tool_choice": {"type": "function", "function": {"name": "get_weather"}},
}

openai_response = openai_client.chat.completions.create(
    **{**kwargs, "model": "gpt-3.5-turbo"}
)
openai_args = json.loads(
    openai_response.choices[0].message.tool_calls[0].function.arguments
)
# somehow magically openai now uses Fahrenheits instead of imperial
assert openai_args == {
    "return": {"data": {"city": "San Francisco", "temperature": "Fahrenheit"}}
}, openai_args
