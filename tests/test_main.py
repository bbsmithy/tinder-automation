import unittest
from tests.context import mobile_login


class TestMain(unittest.TestCase):

    def test_mobile_login(self):
        status = mobile_login('+353838100085')
        self.assertEquals(status, 200)


if __name__ == "__main__":
    unittest.main()
