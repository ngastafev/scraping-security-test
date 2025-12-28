import asyncio
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import time

# Настройки Selenium (headless для скорости)
def get_selenium_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

def scrape_with_bs(url):
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else "No title"
        # Пример: если мало контента — считаем, что BS не справился
        if len(soup.get_text(strip=True)) < 100:
            return None  # переключиться на Selenium
        return {"method": "bs4", "url": url, "title": title, "text_len": len(soup.get_text())}
    except Exception as e:
        # print(f"BS failed for {url}: {e}")
        return None

def scrape_with_selenium_sync(url):
    driver = None
    try:
        driver = get_selenium_driver()
        driver.get(url)
        time.sleep(2)  # ждём JS
        title = driver.title or "No title"
        text = driver.find_element("tag name", "body").text
        return {"method": "selenium", "url": url, "title": title, "text_len": len(text)}
    except Exception as e:
        # print(f"Selenium failed for {url}: {e}")
        return {"method": "failed", "url": url, "error": str(e)}
    finally:
        if driver:
            driver.quit()

async def scrape_url(url, executor):
    loop = asyncio.get_running_loop()
    # Сначала пробуем BS
    result = scrape_with_bs(url)
    if result is not None:
        return result
    # Если BS не дал результата — используем Selenium в потоке
    result = await loop.run_in_executor(executor, scrape_with_selenium_sync, url)
    return result

async def main(urls):
    with ThreadPoolExecutor(max_workers=3) as executor:  # Selenium — ресурсоёмкий
        tasks = [scrape_url(url, executor) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

# === Тест ===
if __name__ == "__main__":
    test_urls = [
        "https://example.com",           # простая статика → BS сработает
        "https://httpbin.org/html",      # тоже статика
        "https://www.python.org",        # может сработать BS
    ]

    results = asyncio.run(main(test_urls))
    for r in results:
        print(r)