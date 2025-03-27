import re
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.common.by import By

def extract_job_data(job):
    # 1. rec_link 요소에서 href를 가져와서 rec_idx 추출 후 전체 링크 생성
    try:
        # id가 "rec_link_..."인 a 태그를 찾음
        link_elem = job.find_element(By.CSS_SELECTOR, "a[id^='rec_link_']")
        href = link_elem.get_attribute("href")
        # 예: "/zf_user/jobs/relay/view?view_type=list&rec_idx=50046280"
        parsed = urlparse(href)
        qs = parse_qs(parsed.query)
        rec_idx = qs.get("rec_idx", [None])[0]
        
        # 고정 URL의 나머지 파라미터들
        recommend_ids = "eJxtkLsRA0EIQ6txLn5aiF3I9d%2BFuRt72cDhG4kHQwBioXKlrNd6B6BVkKugjV4pmTttjGafsilVJyUlsLHCiBoVIzR%2BKXtpmv3By586yQTHrSrwr%2Bze7BA%2FUpqcZ7L2bJdh1d5BT9ZgP0Byrq4V61BJrqoTUx7zB9%2FGREc%3D"
        base_url = "https://www.saramin.co.kr" + parsed.path
        query_str = (
            f"isMypage=no&rec_idx={rec_idx}&recommend_ids={recommend_ids}"
            f"&view_type=list&gz=1&t_ref_content=general&t_ref=jobcategory_recruit"
            f"&relayNonce=d254065fcd7320e99eec&immediately_apply_layer_open=n"
        )
        full_link = f"{base_url}?{query_str}#seq=0"
    except Exception as e:
        print("링크 추출 에러:", e)
        full_link = None

    # 2. 회사명 추출: (주)나비프라
    try:
        company_elem = job.find_element(By.CSS_SELECTOR, ".company_nm a")
        company_name = company_elem.text.strip()
    except Exception as e:
        print("회사명 추출 에러:", e)
        company_name = None

    # 3. 공고 제목 추출
    try:
        title_elem = job.find_element(By.CSS_SELECTOR, ".job_tit a")
        job_title = title_elem.text.strip()
    except Exception as e:
        print("공고 제목 추출 에러:", e)
        job_title = None

    # 4. 마감일 추출 및 가공
    try:
        deadline_elem = job.find_element(By.CSS_SELECTOR, ".support_info .date")
        deadline_text = deadline_elem.text.strip()  # 예: "~03.21(금)" 또는 "상시채용" 등
        # 만약 "채용시" 또는 "상시"라는 문구가 있으면 None 처리
        if "채용시" in deadline_text or "상시" in deadline_text:
            deadline_date = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
        else:
            # "~03.21(금)" 에서 "03.21" 부분을 추출
            m = re.search(r"~?(\d{1,2}\.\d{1,2})", deadline_text)
            if m:
                mmdd = m.group(1)  # 예: "03.21"
                current_year = datetime.now().year
                month, day = mmdd.split(".")
                month = month.zfill(2)
                day = day.zfill(2)
                deadline_date = f"{current_year}-{month}-{day}"
            else:
                deadline_date = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
    except Exception as e:
        print("마감일 추출 에러:", e)
        deadline_date = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")

    # 5. 등록일(지원 등록일) 추출 및 가공
    try:
        reg_elem = job.find_element(By.CSS_SELECTOR, ".support_info .deadlines")
        reg_text = reg_elem.text.strip()  # 예: "1시간 전 등록", "30분 전 등록", "2일 전 등록"
        if "시간 전 등록" in reg_text or "분 전 등록" in reg_text:
            reg_date = datetime.now().strftime("%Y-%m-%d")
        elif "일 전 등록" in reg_text:
            m = re.search(r"(\d+)\s*일 전 등록", reg_text)
            if m:
                days = int(m.group(1))
                reg_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            else:
                reg_date = None
        else:
            reg_date = None
    except Exception as e:
        print("등록일 추출 에러:", e)
        reg_date = None

    return {
        "회사명": company_name,
        "공고 제목": job_title,
        "등록일": reg_date,
        "마감일": deadline_date,
        "공고 링크": full_link
    }
