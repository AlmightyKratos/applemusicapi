from fastapi.responses import JSONResponse
from starlette import status
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from stuff2 import get_all_songs_df, get_duplicate_songs


app = FastAPI()
origins = [
    "http://localhost:3000",
    "https://applemusicstats.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"greeting": "Hello, World!1", "message": "Welcome to FastAPI!"}


class DuplicateSong(BaseModel):
    Name: str
    Artist: str
    len: int


@app.post("/api/duplicates", response_model=list[DuplicateSong])
async def duplicates(file: UploadFile):
    contents = await file.read()
    print(file.content_type)
    if file.content_type != "text/xml":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Invalid file type, must be xml",
        )
    df = get_all_songs_df(contents)
    data = get_duplicate_songs(df)
    return JSONResponse(content=data.to_dicts())
