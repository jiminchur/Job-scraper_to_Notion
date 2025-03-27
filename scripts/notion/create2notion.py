import os
from notion_database.database import Database
from notion_database.properties import Properties
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
PAGE_ID = os.getenv("NOTION_PAGE_ID")

# 데이터베이스 속성 정의
PROPERTY_DICT = {
    "title": "회사명",
    "rich_text": "공고 제목",
    "start_date": "등록일",
    "end_date": "마감일",
    "url": "공고 링크"
}
DATABASE_NAME = 'DataEngineer work list'

# Notion 데이터베이스 생성 함수
def create_database(parent_page_id, title, properties, is_inline=False):
    D = Database(integrations_token=NOTION_API_KEY)
    PROPERTY = Properties()
    for prop_type, prop_name in properties.items():
        if prop_type in ['title', 'rich_text', 'number', 'select', 'multi_select',
                            'checkbox', 'url', 'email', 'phone_number', 'files']:
            getattr(PROPERTY, f"set_{prop_type}")(prop_name)
        elif prop_type in ['date', 'start_date', 'end_date']:
            PROPERTY.set_date(prop_name)

    D.create_database(page_id=parent_page_id, title=title, properties=PROPERTY, is_inline=is_inline)
    return D.result

if __name__ == '__main__':
    new_db = create_database(PAGE_ID, DATABASE_NAME, PROPERTY_DICT, is_inline=True)
    print(new_db)
