import requests,time,re
import  os
from urllib import parse
from bs4 import BeautifulSoup
#屏蔽https报错
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
 
 
proxies={
'http':'127.0.0.1:8080',
'https':'127.0.0.1:8080',
}
header = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cache-Control': 'max-age=0',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '211',
    'Origin': 'https://www.t00ls.com',
    'Referer': 'https://www.t00ls.com/login.html',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Ch-Ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Connection': 'close',
  }

username = 'username'
password = 'password_md5_hash'
login_url = 'https://www.t00ls.com/logging.php?action=login&loginsubmit=yes&floatlogin=yes&inajax=1&inajax=1' #国内    #国外 https://www.t00ls.net/login.html
sign_in_url = 'https://www.t00ls.com/members-profile-xxxxx.html'#修改成自己的签到页面
qiandao_url = 'https://www.t00ls.com/ajax-sign.json'
sign_data = {
    'username' : username,
    'password' : password,
    'questionid': 0,
    'loginfield': 'username'
}
s = requests.session()
#  登录
def login():
    s.post(url=login_url,data=sign_data,verify=False,headers=header,timeout=50)
# 获取签到页面的数据
def sign_page_text():
    sign_page_text = s.get(sign_in_url, verify=False).text
    return sign_page_text
# 签到
def qian_dao(page_text):
    soup = BeautifulSoup(page_text,'html.parser')
    qiandao = soup.find_all('input',{'class': 'btn signbtn'})
    test1=len(qiandao)
    try:
        a = qiandao[1]['value']
        if qiandao[1]['value'] == '签到领TuBi':
            qiandao_onclick = re.findall('\(\'(.*)\'\)', qiandao[1]['onclick'])
        elif '已签到' in qiandao[1]['value']:
            return
        qiandao_data = {
            'formhash':qiandao_onclick[0],
            'signsubmit':'apply'
        }
        qiandao_state = s.post(url=qiandao_url,data=qiandao_data,verify=False,timeout=50).text
        print(qiandao_state)

        if 'success' in qiandao_state:
            return 1
        else:
            return 0

    except:
        exit(print(r'未知错误，登录不成功！请先确认账号密码是否正确！'))

# 获取已签到的天数
def get_qiandao_days(sign_in_later_page):
    soup = BeautifulSoup(sign_in_later_page,'html.parser')
    days = soup.find_all('input',{'class':'btn signbtn'})[1]['value']
    return days
# 自动签到log
log_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'log.txt'

def log(time,result):
    with open(log_file,'a+') as f:
        f.write(f'{time}       {result}\n')

if __name__ == '__main__':
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    login()
    qiandao_text_before = sign_page_text()
    qiandao_result = qian_dao(page_text=qiandao_text_before)
    qiandao_text_later = sign_page_text()
    result = get_qiandao_days(sign_in_later_page=qiandao_text_later)
    if qiandao_result == 1:
        qiandao_stat = f'签到成功: {result}'
        print(qiandao_stat)
        log(start_time,qiandao_stat)
    else:
        qiandao_stat = f'签到失败，不可重复签到: {result}'
        print(qiandao_stat)
        log(start_time, qiandao_stat)
