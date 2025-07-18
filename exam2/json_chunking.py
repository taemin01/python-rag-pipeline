import chromadb
from chromadb.config import Settings
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from module.clean_text import clean_text_for_rag

def get_embeddings_model():
    """
    HuggingFace 임베딩 모델을 반환합니다.
    """
    embeddings_model = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-MiniLM-L6-v2',
            model_kwargs={'device':'cpu'},
            encode_kwargs={'normalize_embeddings':True},
        )
    return embeddings_model

def get_chromadb_collection(json_file):
    """
    ChromaDB 컬렉션을 반환합니다.
    컬렉션 이름은 파일 경로 기반으로 생성됩니다.
    """
    load_dotenv('../RAG_Pipeline/.env')

    client = chromadb.HttpClient(
            host=os.getenv('CHROMADB_HOST'),
            port=os.getenv('CHROMADB_PORT'),
            settings=Settings(anonymized_telemetry=False)
        )

    # JSON 파일 이름을 기반으로 컬렉션 이름 생성
    collection_name = f'document_{os.path.basename(json_file)[0]}'
    print(f"ChromaDB 컬렉션 이름: {collection_name}")

    collection = client.get_or_create_collection(name=collection_name)
    return collection

if __name__ == "__main__":
    """
    Upstage Document Parse JSON 파일을 로드하고, 헤더/푸터를 제외한 본문 내용을 처리합니다.
    청킹 및 임베딩 후 ChromaDB에 적재하며, 시작/끝 페이지 메타데이터만 포함합니다.
    """
    # JSON 파일 경로 설정
    json_file_path = '../RAG_Pipeline/json/A 한화생명 간편가입 암보험.json'

    embeddings_model = get_embeddings_model()
    collection = get_chromadb_collection(json_file_path)

    # JSON 파일 로드
    with open(json_file_path, 'r', encoding='utf-8') as f:
        parsed_data = json.load(f)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n"],
        is_separator_regex=False
    )

    # 페이지별로 텍스트를 모으기 위한 딕셔너리
    pages_content = {}
    # 페이지별로 원본 JSON 요소의 메타데이터를 저장하기 위한 딕셔너리
    pages_metadata = {}

    # elements 배열에서 텍스트 추출
    for element in parsed_data.get('elements', []):
        if not isinstance(element, dict):
            continue

        category = element.get('category')
        page_number = element.get('page')
        
        # 헤더와 푸터 제외
        if category in ['header', 'footer']:
            continue

        # content에서 text 필드 추출
        content = element.get('content', {})
        # content가 딕셔너리 타입이어야 하며 content안에 text 필드가 있어야 추출을 해준다.
        if isinstance(content, dict) and 'text' in content:
            text = content['text']
            
            # 페이지별로 텍스트를 정리하는 로직
            if page_number not in pages_content:
                pages_content[page_number] = []
                pages_metadata[page_number] = {'start_page': page_number, 'end_page': page_number}
            
            pages_content[page_number].append(text)

    if not pages_content:
        print("경고: 처리할 수 있는 텍스트 컨텐츠가 없습니다.")
        sys.exit(1)

    # 페이지 번호 순서대로 처리
    sorted_pages = sorted(pages_content.keys())
    total_chunks = 0

    # 파일 이름에서 문서 ID 추출 (확장자 제외)
    document_id = os.path.splitext(os.path.basename(json_file_path))[0]
    print(f"\n=== 처리 시작: {document_id} ===")

    for page_number in sorted_pages:
        # 문맥 유지를 위해 같은 페이지의 텍스트를 모두 합치기
        combined_page_text = "\n\n".join(pages_content[page_number])
        cleaned_text = clean_text_for_rag(combined_page_text)

        print(f"\n--- 페이지 {page_number} 처리 중 ---")

        # 청킹
        chunks = text_splitter.split_text(cleaned_text)
        total_chunks += len(chunks)
        
        start_page = pages_metadata[page_number]['start_page']
        end_page = pages_metadata[page_number]['end_page']

        for chunk_idx, chunk in enumerate(chunks):
            embedding = embeddings_model.embed_query(chunk)

            metadata = {
                'document_id': document_id,
                'start_page': start_page,
                'end_page': end_page,
            }

            # 고유 ID 생성 (문서ID_페이지번호_청크인덱스)
            chunk_id = f"{document_id}_page_{page_number}_chunk_{chunk_idx+1}"

            collection.add(
                embeddings=[embedding],
                documents=[chunk],
                ids=[chunk_id],
                metadatas=[metadata]
            )

    print(f"\n=== 처리 완료: {document_id} ===")
    print(f"총 처리된 페이지 수: {len(sorted_pages)}")
    print(f"총 생성된 청크 수: {total_chunks}")