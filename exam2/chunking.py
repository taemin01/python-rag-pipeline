import chromadb
from chromadb.config import Settings
import os
import sys
# 모듈을 가져올 경로를 동적으로 추가하는 역할을 한다.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from module.clean_text import clean_text

def get_embeddings_model():
    embeddings_model = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-MiniLM-L6-v2', # 한국어 자연어 추론에 최적화된 모델
            model_kwargs={'device':'cpu'}, # 모델이 CPU에서 실행되도록 설정 GPU를 사용할 수 있다면 cuda로 설정
            encode_kwargs={'normalize_embeddings':True}, # 임베딩을 정규화하여 모든 벡터가 같은 범위 값을 갖도록 한다.
        )
    return embeddings_model

def get_chromadb_collection(file_path):

    load_dotenv('../RAG_Pipeline/.env')

    client = chromadb.HttpClient(
            host=os.getenv('CHROMADB_HOST'), 
            port=os.getenv('CHROMADB_PORT'), 
            settings=Settings(anonymized_telemetry=False)
        )


    # pdf_path = '../RAG_Pipeline/docs/A 한화생명 간편가입 암보험.pdf'
    pdf_path = file_path
    collection_name = f'document_{os.path.basename(pdf_path)[0]}'  # 파일 이름의 앞 알파벳이 추출됨
    print(collection_name)

    collection = client.get_or_create_collection(name=collection_name)
    return collection



"""
1. 문서 로드
2. 청킹
3. 정규식, 전처리 파일은 module/clean_text.py 파일
4. 임베딩 후 chromaDB에 적재 과정을 진행
"""
pdf_path = '../RAG_Pipeline/docs/A 한화생명 간편가입 암보험.pdf'

# embeddings_model = get_embeddings_model()

# collection = get_chromadb_collection(pdf_path)

loader = PyMuPDFLoader(pdf_path)
pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,        # 청크 크기
    chunk_overlap=200,      # 청크 간 중복
    length_function=len,
    separators=["\n\n", "\n", ".", ","],
    is_separator_regex=False
)

for i, page in enumerate(pages):
    text = clean_text(page.page_content)

    chunk = text_splitter.split_text(text)
    print(f'{i + 1}번쨰 청크 : ')
    print(f'{chunk[0]}\n\n')

    # embedding = embeddings_model.embed_query(chunk[0])
    # print(embedding)

    # """
    # 현재 문제 -> 메타데이터로 원본 문서의 해당 페이지를 어떻게 줄 것인지에 대해 고민해보기
    # """
    # collection.add(
    #     embeddings = [embedding],
    #     documents = [chunk[0]],
    #     ids = [f"chunk_{i}"],
    #     metadatas = {
    #         page: i+1
    #     }
    # )