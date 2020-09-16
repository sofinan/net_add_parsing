from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def check_if_ip_addr(ip_addr):
    import re
    pattern = re.compile('\d*\.\d*\.\d*\.\d*')
    if pattern.match(ip_addr):
        return 1
    return 0

def get_ip_addr_ip(WEB_URL):
    driver = webdriver.Firefox()
    driver.get(WEB_URL)
    driver.find_element_by_xpath("//*[@id='xf2']/option[text()='SSL-']").click()
    driver.find_element_by_xpath("//*[@id='xf5']/option[text()='HTTP']").click()
    driver.find_element_by_xpath("//*[@id='xpp']/option[text()='500']").click()
    ip_port_mas = []

    for i in range(4, 450):
        try:
            res = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[" + str(i) + "]/td[1]/font").get_attribute('outerHTML')
            res = remove_html_tags(res)
            pos = res.find("document.write")
            ip_addr = res[:pos]
            pos = res.rfind(":")
            port = res[pos + 1:]
            if check_if_ip_addr(ip_addr) and port.isdigit():
                print(ip_addr, " ", port)
        except:
            print("No IP and port found")

get_ip_addr_ip("https://spys.one/proxys/RU/")