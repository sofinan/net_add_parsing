from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

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

def get_to_site_through_proxy(ip_addr, port, w_url):
    proxy = str(ip_addr) + ":" + str(port)
    caps = webdriver.DesiredCapabilities.FIREFOX
    caps['marionette'] = True

    caps['proxy'] = {
        "proxyType": "MANUAL",
        "sslProxy": proxy,
        'httpProxy': proxy,
    }

    driver = webdriver.Firefox(capabilities=caps)
    driver.set_page_load_timeout(120)
    try:
        driver.get(w_url)
        driver.quit()
        return 1
    except:
        print("Page load Timeout Occured. Quiting !!!")
        driver.quit()
        return 0

def get_ip_addr_ip(WEB_URL):
    driver = webdriver.Firefox()
    driver.get(WEB_URL)
    # if you want to use clear http without ssl uncomment next and comment next next
    # driver.find_element_by_xpath("//*[@id='xf2']/option[text()='SSL-']").click()
    driver.find_element_by_xpath("//*[@id='xf2']/option[text()='SSL+']").click()
    driver.find_element_by_xpath("//*[@id='xf5']/option[text()='HTTP']").click()
    driver.find_element_by_xpath("//*[@id='xpp']/option[text()='500']").click()
    ip_port_mas = []

    for i in range(4, 450):
        try:
            print(i)
            res = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[" + str(i) + "]/td[1]/font").get_attribute('outerHTML')
            res = remove_html_tags(res)
            pos = res.find("document.write")
            ip_addr = res[:pos]
            pos = res.rfind(":")
            port = res[pos + 1:]
            print(ip_addr, port)
            if check_if_ip_addr(ip_addr) and port.isdigit():
                ip_port_mas.append([ip_addr, port])
        except:
            print("No IP and port found")
    driver.quit()
    return(ip_port_mas)

ip_port_mas = get_ip_addr_ip("https://spys.one/proxys/RU/")

# to loop and determine pause
for item in ip_port_mas:
    print(item[0], item[1])
    get_to_site_through_proxy(item[0], item[1], "https://xn--80aafugyk5a.xn--p1ai")
