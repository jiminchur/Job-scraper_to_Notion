# DataEngineer 채용공고 -> Notion 자동화 시스템
> 매일 22시에 Saramin DataEngineer 채용공고를 크롤링하고, Notion Database에 자동으로 업로드 하는 Github Action 기반 프로젝트입니다.

## 🔧 기능소개 (v1.0.0)
* Saramin 채용 공고 자동 수집 (Selenium 사용)
* 오늘 등록된 공고만 필터링하여 저장
* Notion API로 공고를 자동 업로드
* GitHub Actions를 통해 매일 22시에 자동 실행
* JSON 파일은 `data/년-월` 폴더로 구조화 저장

## 🗂️ 프로젝트 구조
```
project/
├── .github/workflows/
│     └── workflow.yml
├── requirements/
│     └── requirements.txt
├── scripts/
│     ├── notion/
│     │     ├── insert2notion.py
│     │     └── create2notion.py
│     └── saramin/
│           ├── job_data.py
│           └── saramin.py
├── data/
│     └── 2025-03/ (자동 생성)
│          └── 2025-03-27_job_data.json
└── .env (환경변수 파일)
```

## 🚀 사용법
### 1. 로컬 실행
```
git clone https://github.com/yourname/saramin-to-notion.git
cd saramin-to-notion
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate (Windows)
pip install -r requirements.txt
```
### 2. .env 생성
```
NOTION_API_KEY=your_notion_secret
NOTION_DATABASE_ID=your_database_id
NOTION_PAGE_ID=your_page_id
```
### 3. 실행
```
python3 scripts/saramin/saramin.py
python3 scripts/notion/insert2notion.py
```

## Github Actions 설정
### 💾 저장소 Secrets 등록
|Key|description|
|-----|-----|
|NOTION_API_KEY|Notion API token|
|NOTION_DATABASE_ID|Notion DB ID|
|NOTION_PAGE_ID|Notion Page ID|
### ⏰ 자동화 스케줄
* 매일 22:00 (KST) 에 자동 실행됨
```
# .github/workflows/workflow.yml
on:
  schedule:
    - cron: '0 22 * * *' 
```
## 🤝 기여 및 피드백
>이 레포는 개인용 자동화 프로젝트입니다.
>추가 제안이나 개선 사항은 언제든 이슈로 남겨주세요!
