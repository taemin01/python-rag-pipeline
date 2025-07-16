import re

def clean_text(text):
    """텍스트 전처리 개선"""
    # 페이지 번호 제거
    text = re.sub(r'-\s*\d+\s*-', '', text)
    text = re.sub(r'\s*\d+\s*\n', '', text)
    
    # 불필요한 특수문자 제거
    text = re.sub(r'[•◆▶▷→▪]', '', text)

    # 삭제하고 싶은 특정 문구들
    remove_patterns = [
        r'수고하셨습니다\.?',          
        r'강의를 마쳤습니다\.?',
        r'감사합니다\.?',
        r'이것으로 \d+차시 강의를 마치겠습니다\.?',
        r'다음 시간에 뵙겠습니다\.?',
        r'도로교통법\s*\n',
        # r'^법제처\s*\n',
        r'.*법제처.*\n',
        r'국가법령정보센터\s*\n',
        # r'^\s*\d+\s*$',  # 단독으로 있는 페이지 번호
        r'confusion matrix.*?(?=\n|$)',  # confusion matrix 관련 텍스트
        r'[rR][oO][cC].*?(?=\n|$)',     # ROC 관련 텍스트
    ]
    
    # 모든 패턴을 하나의 정규식으로 결합
    combined_pattern = '|'.join(remove_patterns)
    text = re.sub(combined_pattern, '', text)
    
    # 특수문자 및 기호 제거 법률 PDF에 필요 없음
    # text = re.sub(r'[①-⑮PXYⅠⅡⅢⅣ○]', '', text)  # 원문자, 로마자 등 제거
    # text = re.sub(r'[\u2160-\u2188]', '', text)   # 유니코드 로마 숫자 범위
    # text = re.sub(r'[.,·:≠=≤≥\(\)\[\]\{\}]', '', text)  # 수학 기호, 괄호 등
    # text = re.sub(r'[=\[\]\(\)┌─┐│┘└┼]{2,}', '', text)  # 박스 드로잉 문자
    # text = re.sub(r'[\u2500-\u257F]+', '', text)  # 유니코드 박스 드로잉 문자
    
    # 불필요한 숫자 패턴 제거
    text = re.sub(r'^\d+\.\s*', '', text, flags=re.MULTILINE)
    
    # 알파벳+숫자+특수문자 조합 패턴 제거 <개정 2014. 12. 30>이 등장하지 않는 원인인 정규식
    # text = re.sub(r'[a-zA-Z0-9\s]*?[^\w\s]+[a-zA-Z0-9\s]*', '', text)
    
    # 연속된 공백 정리
    text = re.sub(r'\s+', ' ', text)
    
    # 불필요한 줄바꿈 정리
    text = re.sub(r'\n+', '\n', text)
    
    # URL 패턴 정리
    text = re.sub(r'http\S+\s?', '', text)
    
    return text.strip()