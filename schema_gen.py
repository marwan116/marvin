# this matters because pydantic's model JSON schema generator will return relative references
from pydantic import BaseModel, Field
from pydantic.json_schema import (
    GenerateJsonSchema as _GenerateJsonSchema,
    JsonSchemaMode,
)
from typing import Any
import jsonref

class GenerateJsonSchema(_GenerateJsonSchema):
    schema_dialect = "draft-00"

    def generate(self, schema: Any, mode: JsonSchemaMode = "validation"):
        return schema


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


# use draft-00 to avoid relative references
pydantic_nested_object_json_schema = WeatherResponse.model_json_schema(
    # by_alias=True,
    # ref_template="#/definitions/{model}",
    # schema_generator=GenerateJsonSchema,
    # schema_generator=lambda: {"$schema": "http://json-schema.org/draft-00/schema#"},
)

import json

out = jsonref.loads(json.dumps(pydantic_nested_object_json_schema))
print(jsonref.dumps(out, indent=2))
