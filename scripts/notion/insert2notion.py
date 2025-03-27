import os
import json
from notion_database.page import Page
from notion_database.database import Database
from notion_database.properties import Properties
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")

# Notion 데이터베이스 속성 가져오기
def get_database_properties(database_id):
    D = Database(integrations_token=NOTION_API_KEY)
    D.retrieve_database(database_id=database_id)
    return D.result

# Notion 페이지 생성
def create_database_page(database_id, properties):
    PROPERTY = Properties()
    res = get_database_properties(database_id)

    for k, v in res['properties'].items():
        property_type = v['type']
        if k in properties:
            getattr(PROPERTY, f'set_{property_type}')(k, properties[k])

    P = Page(integrations_token=NOTION_API_KEY)
    P.create_page(database_id=database_id, properties=PROPERTY)
    return P.result

# 파일에서 공고 데이터 불러와서 Notion에 저장
def insert_jobs_to_notion():
    today = datetime.now().strftime("%Y-%m-%d")
    folder = f"../../data/{datetime.now().strftime('%Y-%m')}"
    filepath = f"{folder}/{today}_job_data.json"

    with open(filepath, 'r', encoding='utf-8') as f:
        job_data_lst = json.load(f)

    for job_data in job_data_lst:
        create_database_page(DATABASE_ID, job_data)

if __name__ == '__main__':
    insert_jobs_to_notion()