# 1. 필요한 라이브러리 가져오기
import os
import requests
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 2. API 키 설정
api_key = os.getenv('UPSTAGE_API_KEY')

# 3. PDF 파일 경로 지정
pdf_file = "docs/15차시_빅데이터 이해와 활용 (5).pdf"

# 4. API 설정
url = 'https://api.upstage.ai/v1/document-digitization'
headers = {"Authorization": f"Bearer {api_key}"}

# 5. PDF 파일 열기
files = {"document": open(pdf_file, "rb")}

# 6. 파싱 옵션 설정
data = {
    "ocr": "force",
    "base64_encoding": "['table']",
    "model": "document-parse"
}

# 7. API 호출하여 문서 파싱
response = requests.post(url, headers=headers, files=files, data=data)
parsed_result = response.json()

# 8. 응답 구조와 내용 확인
print("\n=== API 응답 구조 ===")
print(parsed_result.keys())

print("\n=== Content 내용 ===")
print(json.dumps(parsed_result.get('content', {}), indent=2, ensure_ascii=False)[:500])

print("\n=== Elements 내용 ===")
print(json.dumps(parsed_result.get('elements', []), indent=2, ensure_ascii=False))

# 9. 텍스트 스플리터 설정
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

# 10. 파싱된 결과에서 텍스트 추출하고 청킹
# 응답 구조를 확인한 후 실제 텍스트가 있는 키를 사용하여 청킹
# text_content = parsed_result.get('text', '')  # 'text' 키가 있다고 가정
# chunks = text_splitter.split_text(text_content)

# # 11. 청킹된 결과 확인
# print("\n=== 청킹 결과 ===")
# for i, chunk in enumerate(chunks):
#     print(f"\n=== Chunk {i+1} ===")
#     print(chunk[:100] + "...")  # 각 청크의 처음 100자만 출력