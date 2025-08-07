# Python RAG Pipeline

이 프로젝트는 **Retrieval-Augmented Generation (RAG)** 시스템을 구현한 Python 기반 문서 처리 및 질의응답 파이프라인입니다. PDF 문서와 JSON 형태의 구조화된 문서를 처리하여 벡터 데이터베이스에 저장하고, 사용자 질문에 대한 정확한 답변을 제공합니다.

## 주요 기능

- **다양한 문서 형식 지원**: PDF, JSON (Upstage Document Parse 결과)
- **텍스트 청킹**: 문서를 의미 있는 단위로 분할
- **벡터 임베딩**: HuggingFace 기반 임베딩 모델 사용
- **벡터 검색**: ChromaDB를 통한 유사도 기반 검색
- **질의응답**: Upstage Solar Pro API를 통한 답변 생성
- **한국어 최적화**: 한국어 문서 처리에 특화된 설정

## 프로젝트 구조

```
python-rag-pipeline/
├── module/                    # 핵심 모듈
│   ├── chromadb_connection.py # ChromaDB 연결 및 관리
│   ├── clean_text.py         # 텍스트 전처리
│   ├── hugging_face_embeddings.py # 임베딩 모델
│   ├── py_pdf_loader.py      # PDF 로더
│   └── upstage_dp.py         # Upstage Document Parse
├── exam2/                    # 실험 및 테스트 코드
│   ├── chunking.py           # PDF 청킹
│   ├── json_chunking.py      # JSON 청킹
│   ├── vector_search.py      # 벡터 검색
│   ├── chunk_size_test.py    # 청크 크기 테스트
│   └── upstage_dp.py         # Upstage DP 테스트
├── json/                     # JSON 문서 데이터
├── main.py                   # 메인 실행 파일
├── Pipfile                   # Pipenv 의존성 관리
└── README.md                 # 프로젝트 문서
```

## 기술 스택

### 핵심 라이브러리
- **LangChain**: 문서 처리 및 RAG 파이프라인
- **ChromaDB**: 벡터 데이터베이스
- **HuggingFace**: 임베딩 모델 (sentence-transformers/all-MiniLM-L6-v2)
- **PyMuPDF**: PDF 문서 처리
- **Upstage Solar Pro**: LLM API

### 추가 라이브러리
- **unstructured**: 다양한 문서 형식 지원
- **pytesseract**: OCR 기능
- **pdf2image**: PDF 이미지 변환
- **sentence-transformers**: 임베딩 모델

## 설치 및 설정

### 1. 환경 요구사항
- Python 3.9+
- Pipenv

### 2. 의존성 설치
```bash
# 프로젝트 디렉토리로 이동
cd python-rag-pipeline

# Pipenv 환경 생성 및 의존성 설치
pipenv install

# 가상환경 활성화
pipenv shell
```

### 3. 환경 변수 설정
`.env` 파일을 생성하고 다음 변수들을 설정하세요:

```env
# ChromaDB 설정
CHROMADB_HOST=localhost
CHROMADB_PORT=8000
CHROMADB_COLLECTION=your_collection_name

# Upstage API 설정
UPSTAGE_KEY=your_upstage_api_key
```

### 4. ChromaDB 서버 실행
```bash
# ChromaDB 서버 시작 (별도 터미널에서)
chroma run --host localhost --port 8000
```

## 사용 방법

### 1. 문서 처리 및 벡터 저장

#### PDF 문서 처리
```python
# exam2/chunking.py 실행
python exam2/chunking.py
```

#### JSON 문서 처리 (Upstage Document Parse 결과)
```python
# exam2/json_chunking.py 실행
python exam2/json_chunking.py
```

### 2. 벡터 검색 및 질의응답
```python
# exam2/vector_search.py 실행
python exam2/vector_search.py
```

### 3. 청크 크기 테스트
```python
# exam2/chunk_size_test.py 실행
python exam2/chunk_size_test.py
```

## 주요 모듈 설명

### `module/chromadb_connection.py`
ChromaDB 연결 및 컬렉션 관리를 담당합니다.

### `module/hugging_face_embeddings.py`
HuggingFace 기반 임베딩 모델을 설정하고 텍스트를 벡터로 변환합니다.

### `module/clean_text.py`
텍스트 전처리 및 정규화를 수행합니다.

### `exam2/chunking.py`
PDF 문서를 청킹하고 ChromaDB에 저장합니다.

### `exam2/json_chunking.py`
Upstage Document Parse JSON 결과를 처리하고 청킹합니다.

### `exam2/vector_search.py`
사용자 질문에 대한 벡터 검색 및 답변 생성을 수행합니다.

## 특징

### 한국어 최적화
- `sentence-transformers/all-MiniLM-L6-v2` 모델 사용
- 한국어 문서 처리에 특화된 설정
- UTF-8 인코딩 지원

### 효율적인 청킹
- 재귀적 문자 분할 (RecursiveCharacterTextSplitter)
- 청크 크기: 1000자, 중복: 100-200자
- 페이지 정보 메타데이터 보존

### 정확한 검색
- L2 거리 기반 유사도 계산
- 상위 10개 관련 문서 검색
- 페이지 번호 및 청크 정보 제공

## 예제 사용법

1. **문서 처리**:
   ```bash
   cd exam2
   python json_chunking.py
   ```

2. **질의응답**:
   ```bash
   python vector_search.py
   # 질문 입력: "문서 내용에 관한 질문 입력"
   ```