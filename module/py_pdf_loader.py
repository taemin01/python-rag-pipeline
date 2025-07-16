from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from clean_text import clean_text
# from chunk_quality import analyze_chunk_quality

def load_and_split_pdf(pdf_path):
    """PDF 로드 및 청킹"""
    # PDF 로드
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    
    # 메타데이터 설정
    for page in pages:
        # 텍스트 전처리 적용
        page.page_content = clean_text(page.page_content)
    
    # 텍스트 분할 설정
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1100,        # 청크 크기
        chunk_overlap=200,      # 청크 간 중복
        length_function=len,
        separators=[".", "\n\n"] # 분할 기준
    )
    
    # 전체 텍스트를 하나로 합쳐서 분할
    full_text = '\n'.join([page.page_content for page in pages])
    chunks = text_splitter.split_text(full_text)
    
    print(f"\n총 {len(chunks)}개의 청크로 분할되었습니다.")
    
    return chunks

# 테스트
# pdf_path = "docs/도로교통법.pdf"  # PDF 파일 경로
# chunks = load_and_split_pdf(pdf_path)
# print('------ 문제 청크는 제외한 출력 -------')
# for i, chunk in enumerate(chunks):
#     print(f'{i}번째 : {chunk}\n\n')

# print(chunks)