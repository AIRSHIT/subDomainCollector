from selenium import webdriver

#driver = webdriver.PhantomJS(executable_path=r'H:\SEC\Tool\phantomjs\bin\phantomjs.exe')
driver = webdriver.Firefox(executable_path=r"H:\SEC\Tool\phantomjs\bin\geckodriver.exe")
driver.get('http://i.links.cn/subdomain/')
#driver.get('http://www.baidu.com')
element = driver.find_element_by_id('url2')
element.send_keys('nfmedia.com')
#element.submit()
#driver.find_element_by_class_name("quick2_submit").click()

#driver.get_screenshot_as_file('test.png')