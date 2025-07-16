import re
from typing import Tuple

def clean_text(text):
    """텍스트 전처리 개선"""
    # 페이지 번호 제거
    text = re.sub(r'-\s*\d+\s*-', '', text)
    text = re.sub(r'\s*\d+\s*\n', '', text)

    # 불필요 특수문자 제거
    text = re.sub(r'[▪■※□○●◎◇◆△▲▽▼→←↑↓↔〓◁◀▷▶♠♡♣⊙◈▣◐◑☆★]', '', text)

    # 삭제하고 싶은 특정 문구들
    remove_patterns = [
        r'confusion matrix.*?(?=\n|$)',  # confusion matrix 관련 텍스트
        r'[rR][oO][cC].*?(?=\n|$)',     # ROC 관련 텍스트
    ]
    
    # 모든 패턴을 하나의 정규식으로 결합
    combined_pattern = '|'.join(remove_patterns)
    text = re.sub(combined_pattern, '', text)
    
    # 특수문자 및 기호 제거 법률 PDF에 필요 없음
    text = re.sub(r'[①-⑮PXYⅠⅡⅢⅣ○]', '', text)  # 원문자, 로마자 등 제거
    
    # 연속된 공백 정리
    text = re.sub(r'\s+', ' ', text)
    
    # 불필요한 줄바꿈 정리
    text = re.sub(r'\n+', '\n', text)
    
    return text.strip()

def clean_text_for_rag(text):
    """RAG 시스템을 위한 범용 텍스트 전처리"""
    
    # 1. 헤더/푸터 패턴
    header_footer_patterns = [
        # 상단 헤더
        r'^\s*문서\s*관리\s*번호.*$',
        r'^\s*[발신|수신|참조].*:.*$',
        r'^\s*유효기간\s*:.*$',
        r'^\s*보안등급\s*:.*$',
        r'^\s*분류기호\s*:.*$',
        
        # 하단 푸터
        r'^\s*담당자\s*[:|]\s*.*$',
        r'^\s*결재자\s*[:|]\s*.*$',
        r'^\s*연락처\s*[:|]\s*.*$',
        r'^\s*Copyright.*$',
        r'^\s*[Cc]onfidential.*$',
        
        # 페이지 관련
        r'^\s*Page\s*\d+\s*of\s*\d+\s*$',
        r'^\s*\d+\s*/\s*\d+\s*$',
        r'-\s*\d+\s*-',
    ]

    # 2. 본문 시작 부분의 불필요한 패턴
    content_start_patterns = [
        # 번호 체계
        r'^\s*[1-9]\.\s*',           # 1. 2. 3.
        r'^\s*[1-9]\.[1-9]\.\s*',    # 1.1. 1.2.
        r'^\s*[1-9]\.[1-9]\.[1-9]\.\s*',  # 1.1.1.
        r'^\s*[①②③④⑤⑥⑦⑧⑨⑩]\s*',    # 원문자
        r'^\s*[(（]\s*[1-9]\s*[)）]\s*',  # (1) (2)
        r'^\s*[(（]\s*[가-힣]\s*[)）]\s*',  # (가) (나)
        
        # 들여쓰기와 기호로 시작하는 패턴
        r'^\s*[▶▷→▪◾◼•※-]\s*',     # 기호로 시작
        r'^\s*[가-힣]\.\s*',          # 가. 나.
        r'^\s*[ㄱ-ㅎ]\.\s*',          # ㄱ. ㄴ.
        
        # 제목 스타일 패턴
        r'^\s*제\s*\d+\s*조\s*',      # 제1조
        r'^\s*제\s*\d+\s*장\s*',      # 제1장
        r'^\s*제\s*\d+\s*항\s*',      # 제1항
        r'^\s*제\s*\d+\s*절\s*',      # 제1절
        
        # 기타 문서 구조 패턴
        r'^\s*[\[【]\s*[참고|주의|설명|비고|요약|정의|목적|범위|책임|절차]\s*[\]】]\s*',  # [참고], [주의] 등
        r'^\s*<\s*[참고|주의|설명|비고|요약|정의|목적|범위|책임|절차]\s*>\s*',           # <참고>, <주의> 등
    ]

    # 3. 문단 중간의 불필요한 참조 표시
    reference_patterns = [
        r'\[\s*참고\s*\d+\s*\]',      # [참고1]
        r'\[\s*그림\s*\d+\s*\]',      # [그림1]
        r'\[\s*표\s*\d+\s*\]',        # [표1]
        r'\[\s*별표\s*\d+\s*\]',      # [별표1]
        r'\[\s*서식\s*\d+\s*\]',      # [서식1]
        r'\[\s*참조\s*\d+\s*\]',      # [참조1]
    ]

    # 4. 특수문자 및 기호
    special_chars = [
        r'[■※□○●◎◇◆△▲▽▼→←↑↓↔〓◁◀▷▶♠♡♣⊙◈▣◐◑☆★]',
        r'[㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩]',
        r'[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮]',
    ]

    # 모든 패턴 결합
    all_patterns = (header_footer_patterns + 
                   content_start_patterns + 
                   reference_patterns + 
                   special_chars)
    
    combined_pattern = '|'.join(all_patterns)
    
    # 전처리 적용 (줄 단위로 처리)
    cleaned_lines = []
    for line in text.split('\n'):
        cleaned_line = re.sub(combined_pattern, '', line, flags=re.MULTILINE)
        if cleaned_line.strip():  # 빈 줄이 아닌 경우만 추가
            cleaned_lines.append(cleaned_line)
    
    # 정리된 텍스트 합치기
    text = '\n'.join(cleaned_lines)
    
    # 최종 공백 처리
    text = re.sub(r'\s+', ' ', text)  # 연속된 공백을 하나로
    text = re.sub(r'\n\s*\n', '\n', text)  # 연속된 빈 줄을 하나로
    
    return text.strip()