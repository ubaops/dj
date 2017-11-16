import requests
import json
url="http://clickplus_crm.clickplus.cn/crm_tenant/jump_to_main_url"
data={'id':35}
headers={'Content-Type':'application/json;charset=UTF-8','X-Requested-With':'XMLHttpRequest'}
r1=requests.post(url,data=json.dumps(data),headers=headers)
print(r1.text)