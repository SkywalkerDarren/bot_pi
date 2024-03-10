import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        import re

        def split_sentences(text):
            # 定义一个正则表达式，匹配句子结束符后面的任意非贪婪字符，直到下一个句子结束符
            pattern = r'(.*?[。.！!？?])'
            # 使用正则表达式的findall方法查找所有匹配的子串
            sentences = re.findall(pattern, text, re.DOTALL)
            return sentences

        # 测试函数
        text = "这是一个例句。你好吗？今天天气真好!让我们出去玩。"
        sentences = split_sentences(text)
        for sentence in sentences:
            print(sentence)


if __name__ == '__main__':
    unittest.main()
