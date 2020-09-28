import os
import time
import requests
import io
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import configargparse as argparse

def download(selenium_url, leaf_share_url):
    driver = webdriver.Remote(
        command_executor=selenium_url,
        desired_capabilities=DesiredCapabilities.CHROME,
    )
    driver_ua = driver.execute_script('return navigator.userAgent;')

    driver.get(leaf_share_url)
    while urlparse(driver.current_url).path.startswith('/project'):
        time.sleep(0.1)

    while True:
        try:
            driver.find_element_by_class_name('loading-screen')
            time.sleep(0.1)
        except NoSuchElementException:
            break

    cookies = driver.get_cookies()

    project_url = driver.current_url
    if not project_url.endswith('/'):
        project_url += '/'
    zip_url = urljoin(project_url, 'download/zip')

    ses = requests.Session()
    for cookie in cookies:
        rc = requests.cookies.create_cookie(domain=cookie['domain'], name=cookie['name'], value=cookie['value'])
        ses.cookies.set_cookie(rc)

    headers = {
        'User-Agent': driver_ua,
    }

    bio = io.BytesIO()
    with ses.get(zip_url, headers=headers, stream=True) as r:
        r.raise_for_status()

        for chunk in r.iter_content(chunk_size=8192):
            bio.write(chunk)

    driver.quit()

    return bio.getvalue()
