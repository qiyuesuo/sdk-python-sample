from httpClient.SdkClient import *
from request.ContractDraftRequest import *
from request.ContractSignCompanyRequest import *
from request.ContractSignLpRequest import *
from request.ContractPageRequest import *
from request.DocumentAddByFileRequest import *
from request.DocumentAddByTemplateRequest import *
from request.ContractSendRequest import *
from request.ContractAuditRequest import *
from bean.Stamper import *
from bean.Attachment import *
from bean.Contract import *
from bean.TemplateParam import *
from bean.Action import *
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
根据代码配置生成合同草稿
该场景模拟一个人事合同的场景，即平台方公司与员工签署合同，平台方公司先签署，员工后签
并且指定了平台方公司的内部签署流程：（1）公章签署（2）法人章签署
'''
draft_contract = Contract()
draft_contract.set_subject("合同主题-人事合同")
# 设置签署方 - 平台方公司，tenantName更换为您公司的名称，接收方更正为您公司员工
company_signatory = Signatory()
company_signatory.set_tenantType("COMPANY")
company_signatory.set_tenantName("大头橙橙汁公司")
company_signatory.set_serialNo(1)
company_receiver = User()
company_receiver.set_contact("17621699044")
company_receiver.set_contactType("MOBILE")
company_signatory.set_receiver(company_receiver)
# 设置平台方公司签署流程 - 公章签署流程，并设置该流程应该签署的公章
seal_action = Action()
seal_action.set_type("COMPANY")
seal_action.set_serialNo(1)
seal_action.set_sealId("2490828768980361630")
company_signatory.set_actions([seal_action])
# 设置签署方 - 个人签署方，并设置附件上传要求
personal_signatory = Signatory()
personal_signatory.set_tenantType("PERSONAL")
personal_signatory.set_serialNo(2)
personal_signatory.set_tenantName("邓茜茜")
personal_receiver = User()
personal_receiver.set_contact("15021504325")
personal_receiver.set_contactType("MOBILE")
personal_signatory.set_receiver(personal_receiver)
# 设置合同过期时间
draft_contract.set_expireTime("2020-07-28 23:59:59")
# 不发起合同
draft_contract.set_send(False)
# 请求服务器
draft_response = sdkClient.request(ContractDraftRequest(draft_contract))
# 解析返回数据
draft_mapper = json.loads(draft_response)
if draft_mapper['code'] != 0:
    raise Exception("创建合同草稿失败，失败原因：", draft_mapper['message'])
draft_result = draft_mapper['result']
draft_contractid = draft_result['id']
print('创建合同草稿成功，合同ID：', draft_contractid)

'''
根据本地文件添加合同文档
'''
documentbyfile_request = DocumentAddByFileRequest()
file = open("C:\\Users\\Richard Cheung\\Documents\\契约锁\\测试\\AA.pdf", "rb")
documentbyfile_request.set_file(file)
documentbyfile_request.set_contractId(draft_contractid)
# 将fileSuffix替换为将上传文件正确的文件类型
documentbyfile_request.set_fileSuffix('pdf')
documentbyfile_request.set_title('本地文件上传文档')
# 请求服务器
documentbyfile_response = sdkClient.request(documentbyfile_request)
# 解析返回数据
documentbyfile_mapper = json.loads(documentbyfile_response)
if documentbyfile_mapper['code'] != 0:
    raise Exception('根据本地文件添加合同文档失败，失败原因：', documentbyfile_mapper['message'])
documentbyfile_result = documentbyfile_mapper['result']
file_documentId = documentbyfile_result['documentId']
print('根据本地文件添加合同文档成功，文档ID：', file_documentId)

'''
根据在线模板添加合同文档
'''
documentbytemplate_request = DocumentAddByTemplateRequest()
documentbytemplate_request.set_title('模板上传文档')
documentbytemplate_request.set_contractId(draft_contractid)
documentbytemplate_request.set_templateId('2492236993899110515')
# 若模板为参数模板，设置模板中的参数值
documentbytemplate_request.set_templateParams(
    [TemplateParam('接收方1', '契约锁'), TemplateParam('接收方2', '电子合同')])
# 请求服务器
documentbytemplate_response = sdkClient.request(documentbytemplate_request)
# 解析返回数据
documentbytemplate_mapper = json.loads(documentbytemplate_response)
if documentbytemplate_mapper['code'] != 0:
    raise Exception('根据模板添加合同文档失败，失败原因：', documentbytemplate_mapper['message'])
documentbytemplate_result = documentbytemplate_mapper['result']
template_documentId = documentbytemplate_result['documentId']
print('根据模板添加合同文档成功，文档ID：', template_documentId)

'''
发起合同，并设置签署位置
'''

# 遍历合同详情，查询平台方、个人signatoryId，以及公章签署和法人章签署对应的ActionId
platform_signatoryId = None
personal_signatoryId = None
company_actionId = None

for signatory in draft_result['signatories']:
    if signatory['tenantName'] == '大头橙橙汁公司' and signatory['tenantType'] == 'COMPANY':
        platform_signatoryId = signatory['id']
        for action in signatory['actions']:
            if action['type'] == 'COMPANY':
                company_actionId = action['id']
    if signatory['tenantType'] == 'PERSONAL':
        personal_signatoryId = signatory['id']

# 设置签署位置 - 公章签署
seal_stamper = Stamper()
seal_stamper.set_actionId(company_actionId)
seal_stamper.set_documentId(file_documentId)
seal_stamper.set_type('COMPANY')
seal_stamper.set_offsetX(0.3)
seal_stamper.set_offsetY(0.5)
seal_stamper.set_page(1)


# 设置签署位置 - 时间戳签署
time_stamper = Stamper()
time_stamper.set_actionId(company_actionId)
time_stamper.set_documentId(file_documentId)
time_stamper.set_type('TIMESTAMP')
time_stamper.set_offsetX(0.9)
time_stamper.set_offsetY(0.5)
time_stamper.set_page(1)

# 设置签署位置 - 个人接收方 - 个人签名
personal_stamper = Stamper()
personal_stamper.set_signatoryId(personal_signatoryId)
personal_stamper.set_documentId(file_documentId)
personal_stamper.set_type('PERSONAL')
personal_stamper.set_offsetX(0.4)
personal_stamper.set_offsetY(0.7)
personal_stamper.set_page(1)

# 请求服务器
send_response = sdkClient.request(
    ContractSendRequest(draft_contractid, [seal_stamper, time_stamper, personal_stamper]))
# 解析返回数据
send_mapper = json.loads(send_response)
if send_mapper['code'] != 0:
    raise Exception('发起合同失败，失败原因：', send_mapper['message'])
print('合同发起成功')

'''
公章签署，若发起合同时未指定签署位置需要在此处指定签署位置
'''
seal_signParam = SignParam()
seal_signParam.set_contractId(draft_contractid)
'''
# 指定签署位置 - 公章签署位置
seal_companyStamper = Stamper()
seal_companyStamper.set_documentId(file_documentId)
seal_companyStamper.set_sealId('2490828768980361630')
seal_companyStamper.set_type('COMPANY')
seal_companyStamper.set_offsetX(0.3)
seal_companyStamper.set_offsetY(0.5)
seal_companyStamper.set_page(1)

# 指定签署位置 - 时间戳签署位置
time_companyStamper = Stamper()
time_companyStamper.set_documentId(file_documentId)
time_companyStamper.set_type('TIMESTAMP')
time_companyStamper.set_offsetX(0.5)
time_companyStamper.set_offsetY(0.3)
time_companyStamper.set_page(1)

# 指定签署位置 - 骑缝章签署位置（文档页数大于1页才会生效）
acrosspage_companyStamper = Stamper()
acrosspage_companyStamper.set_documentId(file_documentId)
acrosspage_companyStamper.set_sealId('2490828768980361630')
acrosspage_companyStamper.set_type('ACROSS_PAGE')
acrosspage_companyStamper.set_offsetY(0.7)

seal_signParam.set_stampers([seal_companyStamper, time_companyStamper, acrosspage_companyStamper])
'''
sealsign_response = sdkClient.request(ContractSignCompanyRequest(seal_signParam))
# 解析返回参数
sealsign_mapper = json.loads(sealsign_response)
if sealsign_mapper['code'] != 0:
    raise Exception('公章签署失败，失败原因：', sealsign_mapper['message'])
print('公章签署成功')

'''
平台方签署完成，签署方签署可采用
（1）接收短信的方式登录契约锁云平台进行签署
（2）生成内嵌页面签署链接进行签署（下方生成的链接）
（3）JS-SDK签署（仅支持个人）
'''
page_request = ContractPageRequest(draft_contractid)
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
