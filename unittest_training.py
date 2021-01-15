"""
Python에 포함된 다양한 테스트를 자동화할 수 있는 기능이 포함되어 있는 표준 라이브러리
unittest에 포함된 주요 개념
    - TestCase : unittest 프레임 워크의 테스트 조직의 기본 단위
    - Fixture :
        - 테스트함수의 전 또는 후에 실행
        - 테스트가 실행되기 전에 테스트 환경이 예상 된 상태에 있는지 확인하는 데 사용
        - 테스트 전에 데이터베이스 테이블을 만들거나 테스트 후에 사용한 리소스를 정리하는데 사용
    - assertion :
        - unittest가 테스트가 통과하는지 또는 실패 하는지를 결정.
        - bool test, 객체의 적합성, 적절한 예외 발생 등 다양한 점검을 할 수 있음
        - assertion이 실패하면 테스트 함수가 실패합니다.
"""
import unittest
import os


def custom_function(file_name):
    with open(file_name, 'rt') as f:
        return sum(1 for _ in f)


# Test Case 작성
class CustomTests(unittest.TestCase):
    def setUp(self) -> None:
        """ 테스트 시작 전 파일 작성 """
        self.file_name = 'test_file.txt'
        with open(self.file_name, 'wt') as f:
            f.write("""
            찾아라
            비밀의 열쇠
            미로
            """.strip())

    def tearDown(self) -> None:
        """ 테스트 종료 후 파일 삭제 """
        try:
            os.remove(self.file_name)
        except:
            pass

    def test_runs(self):
        """ 단순 실행 여부 판별하는 테스트 메소드 """
        custom_function(self.file_name)

    def test_line_count(self):
        self.assertEqual(custom_function(self.file_name), 3)


if __name__ == '__main__':
    unittest.main()