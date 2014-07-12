import unittest
from addonpy.addonpyHelpers import AddonHelper
import sys

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
        test_file_path, file_name, file_ext = ('','','')
        
        if sys.platform.startswith('win'):
            test_file_path, file_name, file_ext = (r'c:\test\modules\TestAddon.py','TestAddon','py')
        else:
            test_file_path, file_name, file_ext = (r'/tmp/test/modules/TestAddonInfo.info','TestAddonInfo','info')

        name, ext = AddonHelper.get_basename_and_ext(test_file_path)

        self.assertEqual(file_name, name)
        self.assertEqual(file_ext, ext)        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAddonHelper)
    unittest.TextTestRunner(verbosity=2).run(suite)
