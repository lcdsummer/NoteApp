import unittest
from common.generalAssert import GeneralAssert
from common.caseMsgLogs import class_case_decoration
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from business.businessRe import BusinessRe
from common.yamlRead import YamlRead
import time
import json
from parameterized import parameterized


@class_case_decoration
class SelectCalendarNoteInput(unittest.TestCase):
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

    @parameterized.expand(mustKeys)
    def testCase02_input_mustKey_remove(self, key):
        """查看日历便签接口，input：必填项key缺失"""
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 10
        }
        body.pop(key)
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(412, res.status_code, msg='状态码校验失败')

    @parameterized.expand(mustKeys)
    def testCase03_input_mustKey_remove(self, key):
        """查看日历便签接口，input：必填项的值为空"""
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 10
        }
        body[key] = ""
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(412, res.status_code, msg='状态码校验失败')

    def testCase04_input_remindStartTime_type(self):
        """上传/更新便签内容接口，input：remindStartTime的数值类型校验--长度校验"""
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": 12345678901234567890,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase05_input_remindStartTime_type(self):
        """上传/更新便签内容接口，input：remindStartTime的数值类型校验--传入特殊值  0 """
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": 0,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(412, res.status_code, msg='状态码校验失败')

    def testCase06_input_remindStartTime_type(self):
        """上传/更新便签内容接口，input：remindStartTime的数值类型校验--传入特殊值 -1 """
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": -1,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(412, res.status_code, msg='状态码校验失败')

    def testCase07_input_remindStartTime_type(self):
        """上传/更新便签内容接口，input：remindStartTime的数值类型校验--传入小数"""
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": 1.5,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')

    def testCase08_input_remindStartTime_type(self):
        """上传/更新便签内容接口，input：remindStartTime的数值类型校验--字符串形式的数值校验"""
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": str(remind_time),
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase09_input_remindEndTime_type(self):
        """上传/更新便签内容接口，input：remindEndTime的数值类型校验--长度校验"""
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 12345678901234567890,
            "startIndex": 0,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase10_input_remindEndTime_type(self):
        """上传/更新便签内容接口，input：remindEndTime的数值类型校验--传入特殊值  0 """
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 0,
            "startIndex": 0,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(412, res.status_code, msg='状态码校验失败')

    def testCase11_input_remindEndTime_type(self):
        """上传/更新便签内容接口，input：remindEndTime的数值类型校验--传入特殊值 -1 """
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": -1,
            "startIndex": 0,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(412, res.status_code, msg='状态码校验失败')

    def testCase12_input_remindEndTime_type(self):
        """上传/更新便签内容接口，input：remindEndTime的数值类型校验--传入小数"""
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": (remind_time + 1.5),
            "startIndex": 0,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')

    def testCase13_input_remindEndTime_type(self):
        """上传/更新便签内容接口，input：remindEndTime的数值类型校验--字符串形式的数值校验"""
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": "4102452000000",
            "startIndex": 0,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase14_input_startIndex_type(self):
        """上传/更新便签内容接口，input：startIndex的数值类型校验--长度校验"""
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 12345678901234567890,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase15_input_startIndex_type(self):
        """上传/更新便签内容接口，input：startIndex的数值类型校验--传入特殊值  0 """
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')

    def testCase16_input_startIndex_type(self):
        """上传/更新便签内容接口，input：startIndex的数值类型校验--传入特殊值 -1 """
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": -1,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')

    def testCase17_input_startIndex_type(self):
        """上传/更新便签内容接口，input：startIndex的数值类型校验--传入小数"""
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 1.5,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')

    def testCase18_input_startIndex_type(self):
        """上传/更新便签内容接口，input：startIndex的数值类型校验--字符串形式的数值校验"""
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": "1",
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase19_input_rows_type(self):
        """上传/更新便签内容接口，input：rows的数值类型校验--长度校验"""
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 12345678901234567890
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase20_input_rows_type(self):
        """上传/更新便签内容接口，input：rows的数值类型校验--传入特殊值  0 """
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 0
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')

    def testCase21_input_rows_type(self):
        """上传/更新便签内容接口，input：rows的数值类型校验--传入特殊值 -1 """
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": -1
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(400, res.status_code, msg='状态码校验失败')

    def testCase22_input_rows_type(self):
        """上传/更新便签内容接口，input：rows的数值类型校验--传入小数"""
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 10.5
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(400, res.status_code, msg='状态码校验失败')

    def testCase23_input_rows_type(self):
        """上传/更新便签内容接口，input：rows的数值类型校验--字符串形式的数值校验"""
        # 前置条件：用户"user_id1"下新建一条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": "10"
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')