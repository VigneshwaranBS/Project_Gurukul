from fastapi import FastAPI, Request
import openai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = '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'

@app.post("/prompt")
async def get_prompt(request: Request):
    data = await request.json()
    prompt = data["prompt"]
    print(prompt)
    
    query = f"""
    create a mcq neet question on ${prompt} where it should follow the following format with difficulty level of question range from 1 - 10 .
    Question: your question?

    A.something
    B.someting
    C.somthing
    D.somthing

    Answer: A
    """
    response = await generate_text(query)
    
    return {"response": response}

async def generate_text(prompt):

    # Generate text using OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.6,
    )
    response_str = str(response.choices[0].text.strip())

    # data = formatResponse(response_str)

    # Return generated text
    return response_str

def formatResponse(response_str):
#     # extract question
    question = response_str.split("?\n\n" )[0].replace("Question: ", "")

    # extract answer options
    options = response_str.split("\n\n")[1].split("\n")

    # extract answer
    answer = response_str.split("\n\n")[2].replace("Answer: ", "")

    data = {"question":question, "options": options, "answer":answer}

    # print variables
    print("Question:", question)
    print("Options:", options)
    print("Answer:", answer)
    return data

@app.post("/check-answer")
async def check_answer(request: Request):
    data = await request.json()
    ans = data["answer"]

    if ans:
        prompt = """
        create next question on same topics if i answered the previous question correctly based on difficulty,

        the question should follow the following format
        Question: your question?

        A.something
        B.someting
        C.somthing
        D.somthing

        Answer: A
        """
        response = await generate_text(prompt)

        
    elif ans == False:
        prompt = """
        create next question on same topics if i answered the previous question wrongly based on difficulty  ,

        the question should follow the following format
        Question: your question?

        A. something
        B.someting
        C.somthing
        D.somthing

        Answer: A
        """
        response = await generate_text(prompt)


    return {"response": response}
