import requests
import csv
import xml.etree.ElementTree as ET
import time

keywords = [

]

#confs = ["IEEE S&P", "USENIX Security", "ACM CCS", "NDSS"]
confs = [
    "security and privacy",      # IEEE S&P
    "usenix security",           # USENIX
    "computer and communications security",  # ACM CCS
    "ndss"
]

years = list(range(2020, 2026))

def search_dblp_xml(query, year, conf):
    url = "https://dblp.org/search/publ/api"
    params = {
        "q": f'{query} {conf}',
        "h": "1000",
        "format": "xml"
    }

    response = requests.get(url, params=params)
    root = ET.fromstring(response.text)
    results = []

    for hit in root.findall(".//hit"):
        info = hit.find("info")
        if info is not None:
            title = info.findtext("title")
            link = info.findtext("url")
            year_tag = info.findtext("year")
            if year_tag == str(year):
                results.append((title, link, conf, year))
    return results

all_results = []
for year in years:
    for conf in confs:
        for kw in keywords:
            try:
                papers = search_dblp_xml(kw, year, conf)
                all_results += papers
                print(f"✅ {year} - {conf} - {kw}: {len(papers)} papers")
                time.sleep(1)  # 避免频繁请求被封
            except Exception as e:
                print(f"❌ Error on {year} - {conf} - {kw}: {e}")

# 去重
unique = { (r[0], r[2], r[3]): r for r in all_results }.values()

# 写入 CSV
with open("sca_security_top4_2020_2025.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["标题", "链接", "会议", "年份"])
    w.writerows(unique)

print(f"✅ 总计输出 {len(unique)} 篇论文到 sca_security_top4_2020_2025.csv")
