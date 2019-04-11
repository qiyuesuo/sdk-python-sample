#!/usr/bin/python
# encoding=utf-8
"""
标准签测试合同签署流程
"""
from QysClient import *
from api.StandardSignService import StandardSignService

url = "https://openapi.qiyuesuo.cn"
accessToken = 'tBYw1vOsA3'
accessSecret = 'qLcLpBB4E2Fce3HVgVfiEMwLbeJk75'

qysClient = QysClient(url, accessToken, accessSecret)
standardSignService = StandardSignService(qysClient)
print("----------------------start--------------------")

# # 用PDF文件初始化合同
# file = open("D:/test/NoSign.pdf", "rb")
# docName = "PDF合同文档"
# subject = "PDF合同3"
# initResult = standardSignService.initByFile(file, docName, subject)
# print('initByFile:{contractId:%s}' % initResult['contractId'])
# print('initByFile:{documentId:%s}' % initResult['documentId'])
# # ----------------------initByFile_end--------------------

# 用模板初始化合同
templateId = '2550958037162529700'
templateParams = {"param1":"val1", "param2":"val2"}
docName = "模板合同文档"
subject = '模板合同'
initResult = standardSignService.initByTemplate(templateId, templateParams, docName, subject)
print('initByTemplate:{contractId:%s}' % initResult['contractId'])
print('initByTemplate:{documentId:%s}' % initResult['documentId'])
# ----------------------initByTemplate_end--------------------
#
# # 用html文本初始化合同
# html = '这是html文本创建合同的合同文件内容'
# docName = "HTML合同文档"
# subject = 'HTML合同'
#
# initResult = standardSignService.initByHtml(html, docName, subject)
# print('initByHtml:{contractId:%s}' % initResult['contractId'])
# print('initByHtml:{documentId:%s}' % initResult['documentId'])
# # ----------------------initByHtml_end--------------------

contractId = initResult['contractId']
documentId = initResult['documentId']

# 添加PDF文档
file = open("D:/test/NoSign.pdf", "rb")
title = "PDF合同文档2"
addDocResult = standardSignService.addDocByFile(contractId, file, title)
print('addDocByFile:{documentId:%s}' % addDocResult['documentId'])
# ----------------------addDocByFile_end--------------------

# 添加模板文档
templateId = '2550958037162529700'
templateParams = {"param1": "val1", "param2": "val2"}
title = "模板合同文档2"
addDocResult = standardSignService.addDocByTemplate(contractId, templateId, templateParams, title)
print('addDocByTemplate:{documentId:%s}' % addDocResult['documentId'])
# ----------------------addDocByTemplate_end--------------------

# 添加HTML文档
html = '这是html文本创建合同的合同文件内容'
title = "HTML合同文档2"

addDocResult = standardSignService.addDocByHtml(contractId, html, title)
print('addDocByHtml:{documentId:%s}' % addDocResult['documentId'])
# ----------------------addDocByHtml_end--------------------

# 发起合同
# stamper1 = {
#     'documentId': documentId,
#     'type': 'SEAL',
#     'page': '1',
#     'offsetX': 0.1,
#     'offsetY': 0.1
# }
receiver1 = {
    'type': 'PLATFORM',
    'ordinal': 1,
    'legalPersonRequired': True,
    # 'stampers': [stamper1]
}
stamper2 = {
    'documentId': documentId,
    'type': 'PERSONAL',
    'page': '1',
    'offsetX': 0.2,
    'offsetY': 0.2
}
receiver2 = {
    'type': 'PERSONAL',
    'name': '宋三',
    'mobile': '13636000000',
    'ordinal': 2,
    'authLevel': 'FULL',
    'stampers': [stamper2]
}
receivers = [receiver1, receiver2]
receiveType = "SEQ"
categoryId = "2278742364627402752"
sn = "001"
standardSignService.send(contractId, receivers, receiveType, categoryId, sn)
# ----------------------send_end--------------------

# 法人章签署
stamper = {
    'documentId': documentId,
    'type': 'LEGAL_PERSON',
    'page': '1',
    'offsetX': 0.1,
    'offsetY': 0.1
}
stampers = [stamper]
standardSignService.signByLpseal(contractId, stampers)
print('法人章签署完成')
# ----------------------signLp_end--------------------

# 公章签署
sealId = '2368692359474958388'
stamper = {
    'documentId': documentId,
    'sealId': sealId,
    'type': 'SEAL',
    'page': '1',
    'offsetX': 0.2,
    'offsetY': 0.1
}
stampers = [stamper]
standardSignService.sign(contractId, stampers)
print('公章签署完成')
# ----------------------sign_end--------------------

# 查询合同详情
contract = standardSignService.detail(contractId)
print('查询合同详情完成', contract)
# ----------------------detail_end--------------------

# 下载合同包
file = open("D:/test/standard_contract.zip", "wb")
file.write(standardSignService.download(contractId))
file.close()
print('合同下载完成')
# ----------------------download_end--------------------

# 下载合同文件
file = open("D:/test/standard_doc.pdf", "wb")
file.write(standardSignService.downloadDoc(documentId))
file.close()
print('合同文件下载完成')
# ----------------------downloadDoc_end--------------------
