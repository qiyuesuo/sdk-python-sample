#!/usr/bin/python
# encoding=utf-8

from QysClient import *
from api.TemplateService import TemplateService

url = "http://openapi.qiyuesuo.net"
accessToken = '7EswyQzhBe'
accessSecret = 'lSTLQLZlnCGkdy6MiOhAzIvfbOYlpU'

qysClient = QysClient(url, accessToken, accessSecret)
templateService = TemplateService(qysClient)
print ("----------------------start--------------------")

templates = templateService.templateList()
print('查询合同模板完成，模板数量： %d' % len(templates))
# ----------------------templateList_end--------------------

template = templateService.templateDetail('2291848536332750874')
print('查询模板详情完成')
# ----------------------templateDetail_end--------------------