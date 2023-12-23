from marvin import ai_model, ai_classifier, ai_fn
from pydantic import BaseModel, Field
from openai import OpenAI
import os
import time
from dotenv import load_dotenv
import marvin

load_dotenv()

client = OpenAI(
    api_key=os.environ["ANYSCALE_API_KEY"],
    base_url="https://api.endpoints.anyscale.com/v1",
)
marvin.settings.openai.api_key = os.environ["ANYSCALE_API_KEY"]
marvin.settings.openai.chat.completions.model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
marvin.settings.openai.chat.completions.temperature = 0.2


class Location(BaseModel):
    """Location model."""

    city: str = Field(
        ...,
        description="The inferred official name of a real city in the United States",
    )
    state_abbreviation: str = Field(
        ..., description="The two-letter state abbreviation"
    )


@ai_fn(client=client, model=marvin.settings.openai.chat.completions.model)
def format_response(text: str) -> Location:
    """Formats the response."""


start = time.time()
out = format_response("The Big Apple")
end = time.time()
print(f"Anyscale function call took {end-start=}s")
print(f"{out=}")


# will fail because anyscale doesn't support object definitions
# object defintion could be framed as a function that returns a dict
# @ai_model(
#     client=client, model=marvin.settings.openai.chat.completions.model, temperature=0.2,
# )
# class Location(BaseModel):
#     """Location model."""

#     city: str = Field(
#         ...,
#         description="The inferred official name of a real city in the United States",
#     )
#     state_abbreviation: str = Field(
#         ..., description="The two-letter state abbreviation"
#     )


# start = time.time()
# out = Location("The Big Apple")
# end = time.time()
# print(f"Anyscale function call took {end-start=}s")
# print(f"{out=}")
