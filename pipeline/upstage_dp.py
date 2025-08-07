import os
import sys
import requests
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv

load_dotenv('../RAG_Pipeline/.env')

file_name = 'B 취업규칙'

pdf_path = f'../RAG_Pipeline/docs/{file_name}.pdf'
api_key = os.getenv('UPSTAGE_KEY_TM')

url = "https://api.upstage.ai/v1/document-digitization"
headers = {"Authorization": f"Bearer {api_key}"}
files = {"document": open(pdf_path, "rb")}
data = {"ocr": "force", "base64_encoding": "['table']", "model": "document-parse"}
response = requests.post(url, headers=headers, files=files, data=data)

response = requests.post(url, headers=headers, files=files, data=data)
 
try:
    response_json = response.json()
    
    with open(f'../RAG_Pipeline/json/{file_name}.json', 'w', encoding='utf-8') as f:
        json.dump(response_json, f, ensure_ascii=False, indent=2)
        print(f"JSON 파일 저장 완료")
except Exception as e:
    print(f"저장 오류 발생{str(e)}")