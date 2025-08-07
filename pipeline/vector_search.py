from chunking import get_embeddings_model, get_chromadb_collection
import os
import sys
# 모듈을 가져올 경로를 동적으로 추가하는 역할을 한다.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
import httpx
import readline  # 입력 처리를 위한 라이브러리
import locale

"""
A 한화생명 간편가입 암보험.json'
B 취업규칙.json'
C 여비규정.json'
D 연구전문원관리세칙.json'
E 인사규정시행세칙.json'
F 계약직근로자연봉관리세칙.json'
G 복지후생규정시행세칙.json'
H 지식제안규정.json'
"""

load_dotenv('../RAG_Pipeline/.env')
pdf_path = '../RAG_Pipeline/json/D 연구전문원관리세칙.json'
file_name = os.path.basename(pdf_path) 
collection = get_chromadb_collection(pdf_path)  

"""
1. 사용자 질문 입력 받기
2. 사용자 질문 임베딩
3. 임베딩 한 질문을 벡터 디비에 검색
4. 검색한 결과(문서 페이지 번호, 참조 청킹 내용)
5. 질문 및 참조문서를 포함한 프롬프트 작성하여 답변 생성의 과정을 진행
"""
# 사용자 질문 반환 함수
def get_user_query():
    # Windows 환경에서 'ko_KR.UTF-8' 대신 'ko_KR' 또는 'Korean'을 시도해야 할 수도 있습니다.
    try:
        locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')
    except locale.Error:
        print("Warning: Could not set locale to 'ko_KR.UTF-8'. Trying 'ko_KR'.")
        try:
            locale.setlocale(locale.LC_ALL, 'ko_KR')
        except locale.Error:
            print("Warning: Could not set locale to 'ko_KR'. Readline input might not work as expected.")

    # readline 설정
    readline.set_completer(None)
    readline.parse_and_bind('set editing-mode emacs')
    
    try:
        query = input("질문을 입력하세요: ").encode('utf-8').decode('utf-8') 
        return query.strip()
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
        exit(0)

def user_query_embedding(user_query):
    embeddings_model = get_embeddings_model()

    user_query_embedding = embeddings_model.embed_query(user_query)
    k = 10 # 검색할 청크 개수

    results = collection.query(
        query_embeddings=[user_query_embedding],
        n_results=k,
        include=['documents', 'metadatas']
    )
    print(f"\n--- 사용자 질문: {user_query} ---\n")

    print("--- 검색된 관련 문서 청크 ---")
    
    # 각 결과에 대해 거리 계산
    for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
        # 현재 문서의 임베딩 계산
        doc_embedding = embeddings_model.embed_query(doc)
        
        # L2 거리 계산 (numpy 사용)
        import numpy as np
        distance = np.linalg.norm(np.array(user_query_embedding) - np.array(doc_embedding))
        
        start_page = metadata.get('start_page', 'N/A')
        end_page = metadata.get('end_page', 'N/A')
        print(f"관련 문서 {file_name} (페이지: {start_page}~{end_page}):")
        print(f"거리: {distance:.4f}")  # 거리 점수 표시 (0에 가까울수록 유사)
        print(f"내용: {doc}")
        print('-------\n')

    return results

def upstage_solar_pro_chat(user_query, results):
    api_key = os.getenv('UPSTAGE_KEY_TM')

    contexts = []

    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        # 메타데이터에서 start_page와 end_page 사용
        start_page = metadata.get('start_page', 'N/A')
        end_page = metadata.get('end_page', 'N/A')
        contexts.append(f"참고문서 {file_name} (페이지: {start_page}~{end_page}):\n{doc}\n")
        

    context_text = "\n".join(contexts)

    prompt = f"""Question: {user_query}

    Reference Context:
    {context_text}

    Instructions:
    1. 제공된 참고 문맥만을 기반으로 답변하세요
    2. 외부 출처나 일반 지식을 포함하지 마세요
    3. 문맥에서 관련 정보를 찾을 수 없다면 "제공된 문맥에는 이에 대한 정보가 없습니다"라고 답변하세요
    4. 답변에서 항상 문맥의 특정 부분을 인용하세요. 인용 시 문서 이름과 페이지 범위를 명확히 언급하세요 (예: "참고문서 A 한화생명 간편가입 암보험.json (페이지: 10~12)에 따르면...")
    5. 확실하지 않은 경우 불확실성을 인정하세요

    Response Format:
    1. 직접적인 답변
    2. 참고 문서 이름 및 페이지 범위 (문맥에 없을 시 포함 X)

    Remember: 제공된 맥락에서 제공된 정보만 사용해야 합니다. 참고 문서 이름과 페이지 명시는 필수입니다. 답변은 보기 좋게 줄바꿈 해주세요
    """

    base_url = "https://api.upstage.ai/v1/chat/completions"
    payload = {
        "model": "solar-pro 2",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # timeout -> context가 길어 5초로는 부족, 60초로 늘려줌
    with httpx.Client(timeout=60.0) as client:
        response = client.post(base_url, headers=headers, json=payload)

    return response

# --- 메인 실행 로직 ---
if __name__ == "__main__":
    user_query = get_user_query()
    embeddings_search_results = user_query_embedding(user_query) # user_query를 인자로 전달
    response = upstage_solar_pro_chat(user_query, embeddings_search_results) # user_query를 인자로 전달

    result = response.json()
    print(f"\n--- 최종 답변 ---")
    print(f"질문 : \n{user_query}\n")
    if 'choices' in result and len(result['choices']) > 0 and 'message' in result['choices'][0] and 'content' in result['choices'][0]['message']:
        print(f"LLM 답변 : \n{result['choices'][0]['message']['content']}")
    else:
        print(f"LLM 답변을 받아오는 데 실패했습니다. 응답: {result}")