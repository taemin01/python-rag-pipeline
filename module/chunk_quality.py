import re

def analyze_chunk_quality(chunk):
    """청크 품질 분석"""
    issues = []
    
    # 최소 길이 확인
    if len(chunk) < 50:
        issues.append("청크가 너무 짧습니다")
    
    # 특수문자 비율 확인
    special_chars = re.findall(r'[^가-힣a-zA-Z0-9\s\.,!?]', chunk)
    if len(special_chars) / len(chunk) > 0.1:  # 특수문자 비율이 10% 이상
        issues.append(f"특수문자 비율이 높습니다: {special_chars[:10]}")
    
    # 의미있는 내용 포함 여부 확인
    if not re.search(r'[가-힣]{2,}', chunk):
        issues.append("한글 문자가 충분하지 않습니다")
    
    # 중복된 문자/단어 패턴 확인
    for pattern in [r'(.)\1{2,}', r'(\w+)(\s+\1){2,}']:
        if matches := re.findall(pattern, chunk):
            issues.append(f"중복 패턴 발견: {matches[0]}")
    
    return issues