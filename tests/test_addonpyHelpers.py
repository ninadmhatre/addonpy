import unittest
from addonpy.addonpyHelpers import AddonHelper


class TestAddonHelper(unittest.TestCase):
    """
    if other 2 tests are running properly, then all of the below methods are already tested!
    """

    @classmethod
    def setUpClass(cls):
        cls.boolean_data = {'true': True, 'True': True, '1': True, 'Yes': True, '': False, 'Test': False}

    def test_convert_string_to_boolean(self):
        # addon_helper = AddonHelper()
        # self.assertEqual(expected, addon_helper.convert_string_to_boolean())
        """
        test to check for converting string to equivalent bools
        """

        for test_bool in self.boolean_data.keys():
            expected = self.boolean_data.get(test_bool)
            actual = AddonHelper.convert_string_to_boolean(test_bool)
            self.assertEqual(expected, actual)

    def test_get_basename_and_ext(self):
        # addon_helper = AddonHelper()
        # self.assertEqual(expected, addon_helper.get_basename_and_ext())
        """
        test to check if works on both platforms...
        """

        test_file_windows = r'c:\test\modules\TestAddon.py'
        test_file_unix = r'/tmp/test/modules/TestAddonInfo.info'

        w_f, w_fe = AddonHelper.get_basename_and_ext(test_file_windows)
        u_f, u_fe = AddonHelper.get_basename_and_ext(test_file_unix)

        self.assertEqual('TestAddon', w_f)
        self.assertEqual('TestAddonInfo', u_f)
        self.assertEqual('py', w_fe)
        self.assertEqual('info', u_fe)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAddonHelper)
    unittest.TextTestRunner(verbosity=2).run(suite)
