import unittest
from addonpy import AddonLoader as loader


class TestAddonLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.load_mgr = loader(verbose=False, recursive=False)
        cls.load_mgr.set_addon_dirs(['./data'])
        cls.load_mgr.load_addons()

    def test_get_instance(self):
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
        actual = self.load_mgr.get_instance('CommandLineAddon')
        self.assertEqual(expected, len(self.load_mgr.get_loaded_addons(list_all=True)))

        expected_name = 'CommandLineAddon'
        expected_version = '1.0.5'

        self.assertEqual(expected_name, actual.get_name())
        self.assertEqual(expected_version, actual.get_version())

    def test_get_loaded_addon_instance(self):
        # addon_loader = AddonLoader(verbose, logger, recursive, lazy_load)
        # self.assertEqual(expected, addon_loader.get_loaded_addon_instance())
        """
        test to check if addons loaded can load/call another addons. static method call
        which gets other addons instances
        """

        from addonpy import AddonLoader
        expected_name = 'CommandLineAddon'
        expected_version = '1.0.5'

        actual = AddonLoader.get_loaded_addon_instance('CommandLineAddon')
        self.assertEqual(expected_name, actual.get_name())
        self.assertEqual(expected_version, actual.get_version())

    def test_get_loaded_addons(self):
        # addon_loader = AddonLoader(verbose, logger, recursive, lazy_load)
        # self.assertEqual(expected, addon_loader.get_loaded_addons(by_type, list_all))
        """
        test to check if loaded addons can be retrieved by their type.
        """

        expected = 1
        actual = len(self.load_mgr.get_loaded_addons(by_type='Type-2'))

        self.assertEqual(expected, actual)

        fail_expected = 0
        fail_actual = len(self.load_mgr.get_loaded_addons(by_type='Nothing'))

        self.assertEqual(fail_expected, fail_actual)

    def test_set_lazy_load(self):
        # addon_loader = AddonLoader(verbose, logger, recursive, lazy_load)
        # self.assertEqual(expected, addon_loader.set_lazy_load(state))
        """
        test to check if lazy_load mode runs as expected. addons are only loaded when they are required.
        """
        self.lazy_load_mgr = loader(verbose=False, recursive=False, lazy_load=True)
        self.lazy_load_mgr.set_addon_dirs(['./data'])
        self.lazy_load_mgr.load_addons()

        self.assertEqual(0, len(self.lazy_load_mgr.get_loaded_addons(list_all=True)))

        actual = self.lazy_load_mgr.get_instance('CommandLineAddon')

        self.assertEqual(1, len(self.lazy_load_mgr.get_loaded_addons(list_all=True)))
        self.assertEqual('CommandLineAddon', actual.get_name())
        self.assertEqual('1.0.5', actual.get_version())

    def test_set_recursive_search(self):
        # addon_loader = AddonLoader(verbose, logger, recursive, lazy_load)
        # self.assertEqual(expected, addon_loader.set_recursive_search(state))
        """
        test to check if recursive module search works as expected.
        """
        self.recursive_load_mgr = loader(verbose=False, lazy_load=False, recursive=True)
        self.recursive_load_mgr.set_addon_dirs(['./data'])
        self.recursive_load_mgr.load_addons()

        self.assertEqual(2, len(self.recursive_load_mgr.get_loaded_addons(list_all=True)))

        actual = self.recursive_load_mgr.get_instance('FileIOAddon')
        self.assertEqual('FileIOAddon', actual.get_name())
        self.assertEqual('Release-1', actual.get_version())

    def test_invalid_addon_load(self):
        """
        test to check if invalid addon raises exception.
        """
        self.lazy_load_mgr = loader(verbose=False, recursive=True, lazy_load=True)
        self.lazy_load_mgr.set_addon_dirs(['./data'])
        self.lazy_load_mgr.load_addons()

        self.assertRaises(ImportError, self.lazy_load_mgr.get_instance, 'InvalidAddon')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAddonLoader)
    unittest.TextTestRunner(verbosity=2).run(suite)
