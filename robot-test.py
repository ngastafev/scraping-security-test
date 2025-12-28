import requests
def check_robots(site):
    url = site.rstrip("/") + "/robots.txt"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            print("✅ robots.txt найден")
            print(r.text[:500])
        else:
            print("❌ robots.txt не найден")
    except Exception as e:
        print("Ошибка:", e)

check_robots("https://ria.ru/")

def check_headers(site):
    r = requests.get(site)
    print("🔐 Заголовки ответа:\n")
    for k, v in r.headers.items():
        print(f"{k}: {v}")

check_headers("https://ria.ru/")

def check_user_agent(site):
    headers = {
        "User-Agent": "Python-requests/2.0"
    }
    r = requests.get(site, headers=headers)
    print("Status code:", r.status_code)
    print("Размер ответа:", len(r.text))

check_user_agent("https://ria.ru/")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
r = requests.get("https://ria.ru/", headers=headers)
print("Status code:", r.status_code)
print("Размер ответа:", len(r.text))

import time

def rate_limit_test(site):
    for i in range(100):
        r = requests.get(site)
        print(f"{i+1}: status {r.status_code}")
        time.sleep(0.3)

rate_limit_test("https://ria.ru/")