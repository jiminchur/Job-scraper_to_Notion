import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.common.by import By
import logging

logging.basicConfig(level=logging.INFO)

# 공고 데이터 추출 함수
def extract_job_data(job):
    # 링크 추출
    try:
        link_elem = job.find_element(By.CSS_SELECTOR, "a[id^='rec_link_']")
        href = link_elem.get_attribute("href")
        parsed = urlparse(href)
        qs = parse_qs(parsed.query)
        rec_idx = qs.get("rec_idx", [None])[0]

        recommend_ids = "eJxtkLsRA0EIQ6txLn5aiF3I9d%2BFuRt72cDhG4kHQwBioXKlrNd6B6BVkKugjV4pmTttjGafsilVJyUlsLHCiBoVIzR%2BKXtpmv3By586yQTHrSrwr%2Bze7BA%2FUpqcZ7L2bJdh1d5BT9ZgP0Byrq4V61BJrqoTUx7zB9%2FGREc%3D"
        base_url = "https://www.saramin.co.kr" + parsed.path
        query_str = (
            f"isMypage=no&rec_idx={rec_idx}&recommend_ids={recommend_ids}"
            f"&view_type=list&gz=1&t_ref_content=general&t_ref=jobcategory_recruit"
            f"&relayNonce=d254065fcd7320e99eec&immediately_apply_layer_open=n"
        )
        full_link = f"{base_url}?{query_str}#seq=0"
    except Exception as e:
        logging.error(f"링크 추출 에러: {e}")
        full_link = None

    # 회사명 추출
    try:
        company_elem = job.find_element(By.CSS_SELECTOR, ".company_nm a")
        company_name = company_elem.text.strip()
    except Exception as e:
        logging.error(f"회사명 추출 에러: {e}")
        company_name = None

    # 공고 제목 추출
    try:
        title_elem = job.find_element(By.CSS_SELECTOR, ".job_tit a")
        job_title = title_elem.text.strip()
    except Exception as e:
        logging.error(f"공고 제목 추출 에러: {e}")
        job_title = None

    # 마감일 추출
    try:
        deadline_elem = job.find_element(By.CSS_SELECTOR, ".support_info .date")
        deadline_text = deadline_elem.text.strip()
        deadline = deadline_text if "채용시" not in deadline_text and "상시" not in deadline_text else None
    except Exception as e:
        logging.error(f"마감일 추출 에러: {e}")
        deadline = None

    # 등록일 추출
    today = datetime.now().strftime("%Y-%m-%d")

    return {
        "회사명": company_name,
        "공고 제목": job_title,
        "공고 링크": full_link,
        "마감일": deadline,
        "등록일": today
    }