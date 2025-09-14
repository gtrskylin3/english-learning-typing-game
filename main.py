from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.responses import FileResponse
import uvicorn
from aiohttp import ClientSession
import random
from googletrans import Translator


# создаём объект переводчика
translator = Translator()
QUOTES_API = 'https://dummyjson.com/quotes/random'

async def request_quotes():
    async with ClientSession() as session:
        async with session.get(QUOTES_API) as response:
            if response.status == 200:
                return await response.json()
    



with open("data/short.txt") as f:
    short_words = [i for i in f.read().splitlines()]

with open("data/medium.txt") as f:
    medium_words = [i for i in f.read().splitlines()]

with open("data/long.txt") as f:
    long_words = [i for i in f.read().splitlines()]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешённые домены
    allow_credentials=True,
    allow_methods=["GET"],  # Разрешённые методы
    allow_headers=["*"],  # Разрешённые заголовки
)


@app.get('/')
async def serve_index():
    return FileResponse("index.html")

@app.get('/get_quotes')
async def get_quotes():
    response = await request_quotes()
    if response:
        quote = response['quote']
        translate = await translator.translate(quote, src="en", dest="ru")
        return {
            "quote": ''.join(str(i).capitalize() for i in quote.split('.'))+'.',
            "author": response["author"],
            "translated_quote": str(translate.text)
            }

@app.get("/get_short")
async def get_short():
    word = random.choice(short_words)
    translate = await translator.translate(word, src="en", dest="ru")
    return {
        "word": word,
        "translated_word": translate.text
    }

@app.get("/get_long")
async def get_long():
    word = random.choice(long_words)
    translate = await translator.translate(word, src="en", dest="ru")
    return {
        "word": word,
        "translated_word": translate.text
    }

@app.get("/get_medium")
async def get_medium():
    word = random.choice(medium_words)
    translate = await translator.translate(word, src="en", dest="ru")
    return {
        "word": word,
        "translated_word": translate.text
    }



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host='0.0.0.0', port=10000)