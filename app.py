from pydantic import BaseModel,ValidationError
from groq import Groq
import os
from dotenv import load_dotenv

class Candidate(BaseModel):
    name:str
    education:str
    exp:int
    skills:list[str]
    projects:str


load_dotenv()
apikey=os.getenv("groq")

client=Groq(api_key=apikey)

response=client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role":"system",
                "content":"You a resume analyser,You want to analyse the candidate resume and give the output in json format,"
                "Give the output with basemodel structure name:str,  education:str, exp:int,  skills:list[str],projects:str ,analyse the input and give in this structure"},
                {"role":"user","content":"My name is Naveen.Im completed B.E ECE.I have two year experience in software development.Im skilled in python,api,system design.I have done a social service platform project using java"}],
                response_format={"type": "json_object"})

jsonoutput=response.choices[0].message.content

# jsonoutput=Candidate(**Candidate)

try:
 Candidate.model_validate_json(jsonoutput)
 print(jsonoutput)
except:
  print("Not its not structures as json format")
