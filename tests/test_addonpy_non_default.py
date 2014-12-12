import os
import unittest
from addonpy.addonpy import AddonLoader as loader
import pdb


class TestAddonLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = False
        cls.load_mgr = loader(verbose=cls.verbose, recursive=True)
        cls.load_mgr.set_addon_dirs(['./user'])
        cls.load_mgr.set_addon_methods(['method_a', 'method_b', 'method_c', '__addon__'])
        cls.load_mgr.set_addon_identifier('Plugin')
        cls.load_mgr.load_addons()
        
    def test_custom_extension_load(self):
        # addon_loader = AddonLoader(verbose, logger, recursive, lazy_load)
        # self.assertEqual(expected, addon_loader.get_instance(addon))
        """
        test if get_instance method works as expected.
        run loader and load all addons from directory and check if particular addon is loaded
        Tests:
         - load_addons() works and works for given directories only
         - search addons works
         - every addon can return its own information
        """

        expected = 1
        actual = self.load_mgr.get_instance('FileIOPlugin')
        self.assertEqual(expected, len(self.load_mgr.get_loaded_addons(list_all=True)))

        expected_name = 'FileIOPlugin'
        expected_version = 'Release-1'

        self.assertEqual(expected_name, actual.get_name())
        self.assertEqual(expected_version, actual.get_version())

        expected = 1
        actual = len(self.load_mgr.get_loaded_addons(by_type='Type-1'))
        self.assertEqual(expected, actual)

    def test_no_extension_load(self):
        # addon_loader = AddonLoader(verbose, logger, recursive, lazy_load)
        # self.assertEqual(expected, addon_loader.get_loaded_addon_instance())
        """
        test to check if addons loaded can load/call another addons. static method call
        which gets other addons instances
        """

        from addonpy.addonpy import AddonLoader
        expected_name = 'CommandLine'
        expected_version = '1.0.5'

        self.load_mgr.set_addon_methods(['execute_user', 'start_user', 'stop_user'])
        self.load_mgr.set_addon_identifier(None, ignore_suffix=True)
        self.load_mgr.load_addons()

        actual = AddonLoader.get_loaded_addon_instance('CommandLine', "")
        self.assertEqual(expected_name, actual.get_name())
        self.assertEqual(expected_version, actual.get_version())

        expected = 1
        actual = len(self.load_mgr.get_loaded_addons(by_type='Type-2'))
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAddonLoader)
    unittest.TextTestRunner(verbosity=2).run(suite)
