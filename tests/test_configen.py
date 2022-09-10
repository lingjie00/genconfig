"""Testing the configen functionality."""
import unittest


class Test(unittest.TestCase):
    """Testing the entry point."""
    # TODO:

    def test_dummy(self: unittest.TestCase) -> None:
        """Dummy test."""
        self.assertEqual(True, True)

    def test_mixture(self):
        """function should be able to read a mixture of config types."""
        pass


if __name__ == "__main__":
    unittest.main()
