from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import datetime
import time
 
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get("https://sys.ndhu.edu.tw/gc/sportcenter/SportsFields/login.aspx")                 # 前往網站
 
browser.implicitly_wait(20)                                                                   # 隱含等待20秒

#############################
#        預先處理資料         #
#############################

search_input = browser.find_element_by_id("MainContent_TextBox1")                             # 帳號
search_input.send_keys("410732013")                                                           # 輸入文字
 
search_input = browser.find_element_by_id("MainContent_TextBox2")                             # 密碼
search_input.send_keys("@yeeyff12") 

search_button = browser.find_element_by_id("MainContent_Button1")                             # 登入
search_button.click()  
 
search_button = browser.find_element_by_id("MainContent_Button2")                             # 新增申請
search_button.click()  


selectTag = Select(browser.find_element_by_id("MainContent_drpkind"))                         # 類型
selectTag.select_by_value('1')                                                                # 籃球
time.sleep(5)                                                                                 # 停五秒 為了確定資料已經選取

selectTag = Select(browser.find_element_by_id("MainContent_DropDownList1"))                   # 場地
selectTag.select_by_value('BSK0B')                                                            # B場
time.sleep(5)

#############################
# 每次開始執行前都要確認搶的時間 #
#############################

#借用日期
today = datetime.date.today()
target = today + datetime.timedelta(days = 13)
label = "%04d/%02d/%02d" %(target.year ,target.month ,target.day) #不依靠自動選擇日期：把這行注解掉 改由下面一行選擇
#label = "2021/05/16"

#因為網站日期設定為readonly 要去解析才能送資料
js='document.getElementById("MainContent_TextBox1").removeAttribute("readonly");' #刪掉唯獨屬性
browser.execute_script(js) 
browser.find_element_by_id('MainContent_TextBox1').clear()                        #清理本來的資料
browser.find_element_by_id('MainContent_TextBox1').send_keys(label)               #輸入要借用的日期

#############################
#         開始搶的部分        #
#############################

#設定計時器
tommorrow = today + datetime.timedelta(days = 1)
now_time = datetime.datetime.now()
tommorrow_time = datetime.datetime.strptime(str(tommorrow)+' '+'00:00:00','%Y-%m-%d %H:%M:%S')
wait_time = int((tommorrow_time - now_time).total_seconds()+1)

#計時器啟動
time.sleep(wait_time) 

search_button = browser.find_element_by_id("MainContent_Button1") # 查尋
search_button.click()

search_button = browser.find_element_by_xpath('//*[@id="MainContent_Table1"]/tbody/tr[16]/td[2]/button') # 點擊申請
search_button.click()

search_input = browser.find_element_by_id("MainContent_ReasonTextBox1")  # 借用原因
search_input.send_keys("練球")  # 輸入文字

search_button = browser.find_element_by_id("MainContent_Button4")
time.sleep(2)         # 模擬人反應時間
search_button.click() # 確定

browser.quit() #退出