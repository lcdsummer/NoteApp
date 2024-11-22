import unittest
from common.generalAssert import GeneralAssert
from common.caseMsgLogs import class_case_decoration
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from business.businessRe import BusinessRe
from common.yamlRead import YamlRead
import time


@class_case_decoration
class GreateNoteContentMajor(unittest.TestCase):
    ga = GeneralAssert()
    dataclean = DataClear()
    datacreate = DataCreate()
    re = BusinessRe()
    apiConfig = YamlRead().api_config()['create_note_content']
    envConfig = YamlRead().env_config()
    user_id1 = envConfig['user_id1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    url = host + apiConfig['path']
    mustKeys = apiConfig['mustKeys']

    def setUp(self) -> None:
        """重置数据"""
        self.dataclean.del_notes(self.user_id1, self.sid1)

    def testCase01_major(self):
        """上传/更新便签内容接口，主流程：用户新建便签内容"""
        # 测试步骤：用户"user_id1"下新建一条便签内容
        noteid = str(int(time.time() * 1000))
        body = {
            "noteId": noteid,
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1,
            "BodyType": 0,
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)

        expect = {
            "responseTime": int,
            "contentVersion": int,
            "contentUpdateTime": int
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())
        # 数据源校验
        ress = self.dataclean.select_list_notes(self.user_id1, sid=self.sid1)
        self.assertEqual(noteid, ress[0], msg='数据源校验失败')

