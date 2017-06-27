#!/usr/bin/python
# encoding=utf-8
'''
标准签测试
'''
from QysClient import *
from api.StandardSignService import StandardSignService
from request.Receiver import Receiver
from request.Stamper import Stamper

url = "http://openapi.qiyuesuo.net"
accessToken = '7EswyQzhBe'
accessSecret = 'lSTLQLZlnCGkdy6MiOhAzIvfbOYlpU'

qysClient = QysClient(url, accessToken, accessSecret)
standardSignService = StandardSignService(qysClient)
documentId = '2311727762229027535'
print ("----------------------start--------------------")

# 用PDF文件创建合同
file = open("D:/test/NoSign.pdf", "rb")
subject = 'PDF文件创建合同'
receivers = []
receiver1 = Receiver(type='PLATFORM', ordinal=1, legalPersonRequired=True)
receivers.append(receiver1)
receiver2 = Receiver(type='COMPANY', name='测试公司', mobile='13636350281', authLevel='FULL', ordinal=2)
receivers.append(receiver2)
receiver3 = Receiver(type='PERSONAL', name='张三', mobile='13636350282', authLevel='BASIC', ordinal=3)
receivers.append(receiver3)
receiveType='SIMUL'

documentId = standardSignService.createByFile(file, subject, receivers, receiveType='SIMUL')
print('createByFile:{documentId:%s}' % documentId)
# ----------------------createByFile_end--------------------

# 用模板创建合同
templateId = '2291848536332750874'
templateParams = {"param1":"参数一","param2":"参数二"}
subject = '模板创建合同'
receivers = []
receiver1 = Receiver(type='PLATFORM', ordinal=1)
receivers.append(receiver1)
receiver2 = Receiver(type='COMPANY', name='测试公司', mobile='13636350280', authLevel='FULL', ordinal=2)
receivers.append(receiver2)
receiver3 = Receiver(type='PERSONAL', name='张三', mobile='13636350280', authLevel='BASIC', ordinal=3)
receivers.append(receiver3)
receiveType='SIMUL'

documentId = standardSignService.createByTemplate(templateId, templateParams, subject, receivers)
print('createByTemplate:{documentId:%s}' % documentId)
# ----------------------createByTemplate_end--------------------

# 用html文本创建合同
html = '这是html文本创建合同的合同文件内容'
subject = 'html文本创建合同'
receivers = []
receiver1 = Receiver(type='PLATFORM', ordinal=1, legalPersonRequired=True)
receivers.append(receiver1)
receiver2 = Receiver(type='COMPANY', name='测试公司', mobile='13636350280', authLevel='FULL', ordinal=2)
receivers.append(receiver2)
receiver3 = Receiver(type='PERSONAL', name='张三', mobile='13636350280', authLevel='BASIC', ordinal=3)
receivers.append(receiver3)
receiveType='SIMUL'

documentId = standardSignService.createByHtml(html, subject, receivers, receiveType='SEQ')
print('createByHtml:{documentId:%s}' % documentId)
# ----------------------createByHtml_end--------------------

# 法人章签署
sealId = '2249772556456296448'
# stamper = Stamper(keyword='协议',offsetX=-0,offsetY=-0)
stamper = Stamper(page=1,offsetX=0.1,offsetY=0.1)

standardSignService.signByLpseal(documentId, stamper)
print('法人章签署完成')
# ----------------------signLp_end--------------------

# 公章签署
sealId = '2249772556456296448'
# stamper = Stamper(keyword='协议',offsetX=-0,offsetY=-0)
stamper = Stamper(page=1,offsetX=0.1,offsetY=0.1)

standardSignService.sign(documentId, sealId, stamper)
print('签署完成')
# ----------------------sign_end--------------------

# 查询合同详情
contract = standardSignService.detail(documentId)
print('查询合同详情完成')
# ----------------------detail_end--------------------

# 下载合同包
file = open("D:/test/standard_contract.zip", "wb")
file.write(standardSignService.download(documentId))
file.close()
print('合同下载完成')
# ----------------------download_end--------------------

# 下载合同文件
file = open("D:/test/standard_doc.pdf", "wb")
file.write(standardSignService.downloadDoc(documentId))
file.close()
print('合同文件下载完成')
# ----------------------downloadDoc_end--------------------

# 查询合同分类
categoryList = standardSignService.categoryList()
print('合同分类查询完成：共 %d 个分类' % len(categoryList))
# ----------------------categoryList_end--------------------