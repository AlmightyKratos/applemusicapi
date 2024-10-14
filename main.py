import datetime
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
    t0 = datetime.datetime.now()
    print("start processing", t0.strftime("%H:%M:%S"))
    contents = await file.read()
    t1 = datetime.datetime.now()
    print(f"t1 - {(t1-t0)}")
    if file.content_type != "text/xml":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Invalid file type, must be xml",
        )
    df = get_all_songs_df(contents)
    t2 = datetime.datetime.now()
    print(f"t2 - {t2-t1} - {(t2-t0)}")
    data = get_duplicate_songs(df)
    t3 = datetime.datetime.now()
    print(f"t3 - {t3-t2} - {(t3-t0)}")
    return JSONResponse(content=data.to_dicts())


class CompressedData(BaseModel):
    data: str


# @app.post("/api/decompress", response_model=list[DuplicateSong])
# async def decompress_data(compressed_data: CompressedData):
#     try:
#         lz = LZString()
#         decompressed = lz.decompressFromBase64(compressed_data.data)

#         if decompressed is None:
#             raise ValueError("Decompression resulted in None")

#         # print("Decompressed content:", decompressed)
#         df = get_all_songs_df(decompressed)
#         data = get_duplicate_songs(df)
#         return JSONResponse(content=data.to_dicts())

#     except Exception as e:
#         error_message = f"Error: {str(e)}\nInput data: {compressed_data.data[:100]}..."
#         print(error_message)
#         raise HTTPException(status_code=400, detail=error_message)
