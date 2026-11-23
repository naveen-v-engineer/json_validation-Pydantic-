
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
import os

load_dotenv()

api_key = os.getenv("groq")

if not api_key:
    raise ValueError("Groq API key not found!")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

# Step 1: Define the expected structure
class CareerGuidance(BaseModel):
    career_name: str
    description: str
    required_skills: list[str]
    learning_duration_months: int
    roadmap: list[str]

# Step 2: Get user input
interest = input("Enter your career interest: ")

# Step 3: Request JSON from the LLM
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a career guidance assistant. "
                "Recommend one suitable technology career. "
                "Return only a JSON object with these fields: "
                "career_name (string), "
                "description (string), "
                "required_skills (array of strings), "
                "learning_duration_months (integer), "
                "roadmap (array of strings). "
                "Do not include Markdown formatting."
            )
        },
        {
            "role": "user",
            "content": interest
        }
    ],
    response_format={"type": "json_object"}
)

# Step 4: Extract the JSON text
json_text = response.choices[0].message.content

# Step 5: Validate using Pydantic
try:
    career = CareerGuidance.model_validate_json(json_text)

    print("\nValidated career guidance:")
    print(career.model_dump_json(indent=2))

except ValidationError as error:
    print("Validation failed:")
    print(error)
