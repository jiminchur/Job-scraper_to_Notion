import os
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import job_data

# Selenium 드라이버 설정
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    return webdriver.Chrome(options=options)

# 공고 수집 및 저장 로직
def fetch_and_save_jobs():
    """

    """
    driver = get_driver()
    url = "https://www.saramin.co.kr/zf_user/jobs/list/job-category?cat_kewd=83&exp_cd=1%2C2&exp_max=2"
    driver.get(url)

    job_listings = driver.find_elements(By.CLASS_NAME, "list_item")
    today = datetime.now().strftime("%Y-%m-%d")

    today_jobs = []
    for job in job_listings:
        job_info = job_data.extract_job_data(job)
        if job_info["등록일"] == today:
            today_jobs.append(job_info)

    folder = f"../../data/{datetime.now().strftime('%Y-%m')}"
    os.makedirs(folder, exist_ok=True)

    filepath = f"{folder}/{today}_job_data.json"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(today_jobs, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    fetch_and_save_jobs()
