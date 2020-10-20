import AI
import unittest
from BeautifulReport import BeautifulReport

class MyTest(unittest.TestCase):
    '''
    有针对性地测试四种情况
    '''
    def test1(self):
        '''step=0'''
        exclude = 5
        challenge = [1, 7, 3, 0, 6, 8, 9, 4, 2]  # 一维列表
        step = 0
        swap = [2, 9]
        print(AI.main(exclude,challenge,step,swap))

    def test2(self):
        '''原图有解且可以在强制交换之前走完'''
        exclude = 2
        challenge = [1, 7, 3, 0, 6, 8, 4, 5, 9]  # 一维列表
        step = 20
        swap = [3, 6]
        print(AI.main(exclude, challenge, step, swap))

    def test3(self):
        '''原图有解但无法在强制交换之前走完'''
        exclude = 2
        challenge = [1, 7, 3, 0, 6, 8, 4, 5, 9]  # 一维列表
        step = 10
        swap = [3, 6]
        print(AI.main(exclude, challenge, step, swap))

    def test4(self):
        '''原图无解'''
        exclude = 9
        challenge = [1, 7, 3, 0, 6, 8, 5, 4, 2]  # 一维列表
        step = 15
        swap = [2, 7]
        print(AI.main(exclude, challenge, step, swap))


if __name__ == "__main__":
    ts = unittest.TestSuite()
    for i in range(1,5):
        testname = 'test'+str(i)
        ts.addTest(MyTest(testname))
    result = BeautifulReport(ts)
    result.report(
        filename='TestReport.html',  # 测试报告名称, 如果不指定默认文件名为report.html
        description='测试',  # 测试报告用例名称展示
        report_dir='report',  # 报告文件写入路径
        theme='theme_default'
    )

