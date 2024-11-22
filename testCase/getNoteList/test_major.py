import unittest
from common.generalAssert import GeneralAssert
from common.caseMsgLogs import class_case_decoration
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from business.businessRe import BusinessRe
from common.yamlRead import YamlRead


@class_case_decoration
class GetNoteListMajor(unittest.TestCase):
    ga = GeneralAssert()
    dataclean = DataClear()
    datacreate = DataCreate()
    re = BusinessRe()
    apiConfig = YamlRead().api_config()['get_note_list']
    envConfig = YamlRead().env_config()
    user_id1 = envConfig['user_id1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    mustKeys = apiConfig['mustKeys']

    def setUp(self) -> None:
        """重置数据"""
        self.dataclean.del_notes(self.user_id1, self.sid1)

    def testCase01_major(self):
        """获取首页便签列表接口，主流程：用户查看首页便签列表"""
        # 前置条件：用户"user_id1"下新建一条便签数据
        note_lists_id = self.datacreate.note_create(1, self.user_id1, self.sid1)
        # 测试步骤：获取user_id1的首页便签列表
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)

        expect = {
            "responseTime": int,
            "webNotes": [
                {
                    "noteId": note_lists_id[0],
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
