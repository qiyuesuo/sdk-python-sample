#!/usr/bin/python
# encoding=utf-8
'''
远程签测试
'''

from QysClient import *
from common.Company import Company
from common.Person import Person
from request.Stamper import *
from api.RemoteSignService import RemoteSignService
from api.SealService import SealService
from common.SignType import SignType

url = "http://openapi.qiyuesuo.net"
accessToken = '7EswyQzhBe'
accessSecret = 'lSTLQLZlnCGkdy6MiOhAzIvfbOYlpU'

qysClient = QysClient(url, accessToken, accessSecret)
remoteSignService = RemoteSignService(qysClient)
sealService = SealService(qysClient)
documentId = '2310004703800135840'
print ("----------------------start--------------------")

# 用本地文件创建合同
file = open("D:/test/NoSign.pdf", "rb")
subject = '本地PDF文件创建合同'
expireTime = "2017-06-10 00:00:00"

documentId = remoteSignService.createByFile(file, subject)
print('createByFile:{documentId:%s}' % documentId)
# ----------------------createByFile_end--------------------

# 用模板创建合同
templateId = '2291848536332750874'
templateParams = {"param1":"参数一","param2":"参数二"}
subject = '模板创建合同'
expireTime = "2017-06-10 00:00:00"
print('createByTemplate:{documentId:%s}' % remoteSignService.createByTemplate(templateId, templateParams, subject))
# ----------------------createByTemplate_end--------------------

# 用html创建合同
html = '这个一个html创建远程签合同的内容'
subject = 'html创建合同'
expireTime = "2017-06-10 00:00:00"
print('createByHtml:{documentId:%s}' % remoteSignService.createByHtml(html, subject))
# ----------------------createByHtml_end--------------------

# 运营方签署
stamper = Stamper(keyword='协议',offsetX=-0.1,offsetY=-0.1)
# stamper = Stamper(page=2,offsetX=0.01,offsetY=0.01)

remoteSignService.signByPlatform(documentId,sealId='2249772556456296448',stamper=stamper)
print('运营方签署完成')
# ----------------------signByPlatform_end--------------------

# 公司用户签署
# stamper = Stamper(keyword='协议',offsetX=0.01,offsetY=0.01)
stamper = Stamper(page=1,offsetX=0.2,offsetY=0.01)
company = Company(name='测试公司', registerNo='123123123')
sealData = sealService.companySeal('测试公司')

remoteSignService.signByCompany(documentId, company, sealData, stamper)
print('公司用户签署完成')
# ----------------------signByCompany_end--------------------

# 个人用户签署
# stamper = Stamper(keyword='协议',offsetX=0.01,offsetY=0.01)
stamper = Stamper(page=11,offsetX=0.3,offsetY=0.01)
person = Person(name='张三', idcard='123123123213')
sealData = sealService.personalSeal('张三')

remoteSignService.signByPerson(documentId, person, sealData, stamper)
print('个人用户签署完成')
# ----------------------signByPerson_end--------------------

# 获取公司用户签署合同链接
company = Company(name='PY-测试公司', registerNo='12321321321321', telephone='13636350280')
stamper = Stamper(keyword='协议', keywordIndex=-1, offsetX=0, offsetY=0)
sealData = sealService.companySeal('PY-测试公司')
signUrlResponse = remoteSignService.signUrl(documentId, SignType.SIGN, company, 'http://www.baidu.com', sealData, stamper)
print('签署合同链接获取完成,company-signUrl: %s ,token: %s' % (str(signUrlResponse.getSignUrl()), str(signUrlResponse.getToken())))
#----------------------signUrl_end--------------------

# 获取个人用户签署合同链接
person = Person(name='张三', idcard='123213213213213', mobile= '13636350280')
stamper = Stamper(keyword='协议', keywordIndex=-1, offsetX=-0.1, offsetY=-0.05)
sealData = sealService.personalSeal('张三')
signUrlResponse = remoteSignService.signUrl(documentId, SignType.SIGN, person, 'http://www.baidu.com', sealData, stamper)
print('签署合同链接获取完成,personal-signUrl: %s ,token: %s' % (str(signUrlResponse.getSignUrl()), str(signUrlResponse.getToken())))
#----------------------signUrl_end--------------------

# 获取查看合同链接
viewUrlResponse = remoteSignService.viewUrl(documentId)
print('签署合同链接获取完成,viewUrl: %s ,token: %s' % (str(viewUrlResponse.getViewUrl()), str(viewUrlResponse.getToken())))
# ----------------------viewUrl_end--------------------

# 合同封存
remoteSignService.complete(documentId)
print('合同封存')
# ----------------------complete_end--------------------

# 查询合同详情
contract = remoteSignService.detail(documentId)
print('查询合同详情完成')
# ----------------------detail_end--------------------

# 下载合同文件
file = open("D:/test/downloadPdf.pdf","wb")
file.write(remoteSignService.download('2309905209611849732'))
file.close()
print('合同下载完成')
# ----------------------download_end--------------------