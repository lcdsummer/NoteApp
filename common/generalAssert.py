import unittest


class GeneralAssert(unittest.TestCase):
    def http_assert(self, expect, actual):
        """
        http返回体通用的断言方法

        :param expect: dict or list，接口返回体的预期值
        :param actual: dict or list，实际结果的获取方式通常可以用 response.json()
        :return: True 断言成功，assert fail 断言失败
        """
        if isinstance(expect, dict):
            # 断言字典的键数量相同
            self.assertEqual(len(expect.keys()), len(actual.keys()), msg=f'返回体字段长度不一致，实际返回的字段有:{list(actual.keys())}')

            for k, v in expect.items():
                # 断言键存在于实际返回体中
                self.assertIn(k, actual.keys(), msg=f'{k}字段不存在于实际返回体')

                # 根据值的类型进行不同的断言
                if isinstance(v, type):
                    # 校验字段的数据类型(字段为动态值)
                    self.assertEqual(v, type(actual[k]), msg=f'{k}字段类型与实际处理的类型不一致，实际返回的参数值: {actual[k]}')
                elif isinstance(v, list):
                    # 校验字段的精确值
                    self.http_assert(expect[k], actual[k])
                elif isinstance(v, dict):
                    self.http_assert(v, actual[k])
                else:
                    self.assertEqual(v, actual[k], msg=f'{k}字段值不一致')
        else:
            # 列表结构的断言方法
            self.assertEqual(len(expect), len(actual), msg=f'返回体字段长度不一致，实际返回的字段有: {actual}')

            for index in range(len(expect)):
                if isinstance(expect[index], type):
                    self.assertEqual(expect[index], type(actual[index]),
                                     msg=f'{expect[index]}字段类型与实际处理的类型不一致，实际返回的参数值: {actual[index]}')
                elif isinstance(expect[index], dict):
                    self.http_assert(expect[index], actual[index])
                elif isinstance(expect[index], list):
                    self.http_assert(expect[index], actual[index])
                else:
                    self.assertEqual(expect[index], actual[index],
                                     msg=f'{expect[index]}字段值不一致，实际返回的参数值: {actual[index]}')

