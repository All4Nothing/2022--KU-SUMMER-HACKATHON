from cmath import nan
from fastapi import FastAPI, UploadFile, File, Request
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel



from fastapi.responses import JSONResponse

class Sound(BaseModel):
    text: str

tokenizer = AutoTokenizer.from_pretrained("eliza-dukim/bert-base-finetuned-sts")

model = AutoModelForSequenceClassification.from_pretrained("eliza-dukim/bert-base-finetuned-sts")

model = model.from_pretrained('model.pt')

contents = ["밝기 설정하는 법", "와이파이 설정하는 법", "음식 시키는 법", "카카오톡 사진 보내기", "이모티콘 사용하는 법", "음량 조절하는 법"] #
threshold = 0.1

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.post("/character/")
async def contents_prediction(speech: Sound):
    similarity = []
    def preprocess_function(s1, s2):
        return tokenizer(s1, s2, truncation=True, max_length=512, padding=True, return_tensors='pt')

    def softmax(x):
        y = np.exp(x - np.max(x))
        f_x = y / np.sum(np.exp(x))
        return f_x
    
    def sentence_to_encoded_dict(input_text):
        for content in contents:
            encoded_dict = preprocess_function(input_text, content)
            input_ids = encoded_dict['input_ids']
            token_type_ids = encoded_dict['token_type_ids']
            attention_mask = encoded_dict['attention_mask']
            pred = model(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
            similarity.append(pred["logits"].item())
            print(pred["logits"].item())

        return similarity

    softmax_var = softmax(sentence_to_encoded_dict(speech.text))
    print(softmax_var)
    
    if softmax_var[np.argmax(softmax_var)] > threshold:
       return {"contents" : contents[np.argmax(softmax_var)]}
    else:
        return {"contents" : "다시 말씀해주세요"}

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )