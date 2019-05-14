import unittest
import main


class TestMain(unittest.TestCase):

    def test_mobile_login(self):
        status = main.mobile_login('+353838100085')
        self.assertEquals(status, 200)


if __name__ == "__main__":
    unittest.main()
