from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embeddings(text):
    embeddings_model = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2', # 한국어 자연어 추론에 최적화된 모델
        model_kwargs={'device':'cpu'}, # 모델이 CPU에서 실행되도록 설정 GPU를 사용할 수 있다면 cuda로 설정
        encode_kwargs={'normalize_embeddings':True}, # 임베딩을 정규화하여 모든 벡터가 같은 범위 값을 갖도록 한다.
    )
    return [embeddings_model.embed_query(chunk) for chunk in text]  # 항상 리스트 반환