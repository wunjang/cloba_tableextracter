# Cloba 테이블 추출기

Cloba OCR API를 사용하여 이미지에서 테이블을 추출하고 CSV 파일로 내보내는 Python 유틸리티입니다.

## 기능

- Cloba OCR API 테이블 추출 요청 자동화
- 추출한 테이블을 CSV 파일로 내보내기

## 요구 사항

- Python 3.13+
- aiohttp 3.11.18+

## 설치

1. 저장소 복제:
```bash
git clone https://github.com/wunjang/cloba-tableextracter.git
cd cloba-tableextracter
```

2. 의존성 설치:
```bash
pip install -e .
```

## 설정

1. 네이버 클라우드 플랫폼에서 클로바 OCR을 사용 신청하세요
2. General 도메인 생성 후 표 추출 여부를 활성화하세요
3. config.json 파일에 얻은 API_KEY와 url을 입력하세요 
```json
{
    "API_KEY": "YOUR_API_KEY",
    "url": "YOUR_API_URL",
    "image_path": "./Images/",
    "output_path": "./Output/",
    "allowed_extensions": [".jpg", ".jpeg", ".png", ".gif"]
}
```

## 사용 방법

### 방법 1: Python 사용

1. 테이블이 포함된 이미지를 Images 폴더에 넣으세요
2. 프로그램 실행:
```bash
python main.py
```
3. Output 폴더에서 추출된 CSV 파일을 확인하세요

### 방법 2: 실행 파일 사용

Python이 설치되어 있지 않은 사용자를 위한 방법:

1. Releases 섹션에서 실행 파일을 다운로드하고 압축을 해제하세요
2. 테이블이 포함된 이미지를 Images 폴더에 넣으세요
3. cloba_tableextracter.exe 파일을 더블 클릭하여 프로그램을 실행하세요
4. Output 폴더에서 추출된 CSV 파일을 확인하세요
