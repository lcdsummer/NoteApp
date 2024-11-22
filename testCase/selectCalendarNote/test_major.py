import unittest
from common.generalAssert import GeneralAssert
from common.caseMsgLogs import class_case_decoration
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from business.businessRe import BusinessRe
from common.yamlRead import YamlRead
import time


@class_case_decoration
class SelectCalendarNoteMajor(unittest.TestCase):
    ga = GeneralAssert()
    dataclean = DataClear()
    datacreate = DataCreate()
    re = BusinessRe()
    apiConfig = YamlRead().api_config()['select_calendar_note']
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
        """查看日历便签接口，主流程：用户查看日历便签"""
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        res_noteid = self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)

        expect = {
            "responseTime": int,
            "webNotes": [
                {
                    "noteId": res_noteid[0],
                    "createTime": int,
                    "star": 0,
                    "remindTime": int,
                    "remindType": int,
                    "infoVersion": int,
                    "infoUpdateTime": int,
                    "groupId": None,
                    "title": "test",
                    "summary": "test",
                    "thumbnail": None,
                    "contentVersion": int,
                    "contentUpdateTime": int
                }
            ]
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())

