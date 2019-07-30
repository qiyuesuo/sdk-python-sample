from httpClient.SdkClient import *
from request.ContractDraftRequest import *
from request.ContractSignCompanyRequest import *
from request.ContractSignLpRequest import *
from request.ContractPageRequest import *
from bean.Contract import *
from bean.Category import *
from bean.TemplateParam import *
from bean.Signatory import *
from bean.User import *
from bean.SignParam import *
import json

'''
初始化契约锁客户端，将accessToken与accessSecret替换为自己的数据值
'''
url = "https://openapi.qiyuesuo.cn"
accessToken = '替换为您开放平台的 App Token'
accessSecret = '替换为您开放平台的 App Secret'
sdkClient = SdkClient(url, accessToken, accessSecret)

'''
根据业务分类发起合同
根据业务分类直接发起合同要求：
（1）业务分类配置签署文件
（2）指定签署位置（可选，若未指定需要在签署时传入签署位置）
（3）若指定了签署流程，创建草稿的签署方必须与业务分类配置相符

该场景模拟一个人事合同的场景，即平台方公司与员工签署合同，平台方公司先签署，员工后签

'''
draft_request = ContractDraftRequest()
draft_contract = Contract()
draft_contract.set_category(Category("2584280095237849689"))
draft_contract.set_subject("合同主题名称")
# 若业务分类中包含参数模板，设置发起方参数内容
draft_contract.set_templateParms([TemplateParam("接收方1", "契约锁"), TemplateParam("接收方2", "电子合同")])
# 设置签署方 - 平台方公司，tenantName更换为您公司的名称，接收方更正为您公司员工
company_signatory = Signatory()
company_signatory.set_tenantType("COMPANY")
company_signatory.set_tenantName("大头橙橙汁公司")
company_signatory.set_serialNo(1)
company_receiver = User()
company_receiver.set_contact("17621699044")
company_receiver.set_contactType("MOBILE")
company_signatory.set_receiver(company_receiver)
# 设置签署方 - 个人签署方
personal_signatory = Signatory()
personal_signatory.set_tenantType("PERSONAL")
personal_signatory.set_tenantName("邓茜茜")
personal_signatory.set_serialNo(2)
personal_receiver = User()
personal_receiver.set_contact("15021504325")
personal_receiver.set_contactType("MOBILE")
personal_signatory.set_receiver(personal_receiver)
draft_contract.set_signatories([company_signatory, personal_signatory])
draft_contract.set_send(True)
# 请求服务端
response = sdkClient.request(ContractDraftRequest(draft_contract))
# 解析返回数据
draft_mapper = json.loads(response)
if draft_mapper['code'] != 0:
    raise Exception('创建合同草稿失败，失败原因：', draft_mapper['message'])
contract = draft_mapper['result']
contractid = contract['id']
print('创建合同草稿成功，合同ID', contractid)

'''
公章签署，此处默认为业务分类已经配置了签署位置且签署节点配置了签署公章，否则需要在此处指定签署位置
'''
response = sdkClient.request(ContractSignCompanyRequest(SignParam(contractid)))
# 解析返回参数
seal_mapper = json.loads(response)
if seal_mapper['code'] != 0:
    raise Exception('公章签署失败，失败原因：', seal_mapper['message'])
print('公章签署成功')

'''
法人章签署，此处默认为业务分类已经配置了签署位置且公司维护了有效的法人章，否则需要在此处指定签署位置
'''
response = sdkClient.request(ContractSignLpRequest(SignParam(contractid)))
# 解析返回参数
lp_mapper = json.loads(response)
if lp_mapper['code'] != 0:
    raise Exception('法人章签署失败，失败原因：', lp_mapper['message'])
print('法人章签署成功')

'''
平台方签署完成，签署方签署可采用
（1）接收短信的方式登录契约锁云平台进行签署
（2）生成内嵌页面签署链接进行签署（下方生成的链接）
（3）JS-SDK签署（仅支持个人）
'''
page_request = ContractPageRequest(contractid)
sign_user = User()
sign_user.set_contact("15021504325")
sign_user.set_contactType("MOBILE")
page_request.set_user(sign_user)
response = sdkClient.request(page_request)
page_mapper = json.loads(response)
if page_mapper['code'] != 0:
    raise Exception('签署链接生成失败，失败原因：', page_mapper['message'])
page_result = page_mapper['result']
print('签署链接签署成功，链接：', page_result['pageUrl'])
