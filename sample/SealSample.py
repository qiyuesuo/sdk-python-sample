#!/usr/bin/python
# encoding=utf-8

from QysClient import *
from api.SealService import SealService

url = "http://openapi.qiyuesuo.net"
accessToken = '7EswyQzhBe'
accessSecret = 'lSTLQLZlnCGkdy6MiOhAzIvfbOYlpU'

qysClient = QysClient(url, accessToken, accessSecret)
sealService = SealService(qysClient)
print ("----------------------start--------------------")

personalSeal = sealService.personalSeal('张三')
print('生成个人印章： %s' % str(personalSeal))
# ----------------------personalSeal_end--------------------

companySeal = sealService.companySeal('测试公司')
print('生成公司印章： %s' % str(companySeal))
# ----------------------companySeal_end--------------------

platformSeal = sealService.platformSeal('2249772556456296448')
print('获取运营方印章： %s' % str(platformSeal.decode('utf-8')))
# ----------------------platformSeal_end--------------------

sealList = sealService.platformSealList()
print('查询平台印章完成：共 %d 个印章' % len(sealList))
# ----------------------platformSealList_end--------------------