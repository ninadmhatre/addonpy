__author__ = 'Ninad'

import unittest
import os

from build.addonpy import AddonLoader


class AddonLoaderTest(unittest.TestCase):
    def setUp(self):
        self.addon_manager = AddonLoader(verbose=True)

    def test_get_addon_config(self):
        """
        Check if default config is picked up if addon-loader.info is not provided
        """
        expected = dict(required_functions=['start', 'stop', 'execute', '__addon__', '__info__'],
                        addon_places=[os.path.abspath(os.curdir)],
                        parse_from_info_file="False")

        self.assertDictEqual(self.addon_manager._load_own_config(), expected, "Config should be same")

    def test_get_addon_count_before(self):
        """
        check addons in current directory
        """
        self.addon_manager.load_addons()

        expected = 0
        actual = self.addon_manager.get_loaded_addons(type_filter='*')
        self.assertEqual(expected, len(actual), "addon directory not set, count should be zero")

    def test_get_addon_count_after(self):
        """
        set addon directory and then check for addons
        """

        new_addon_dir = os.path.abspath(os.path.join('.', 'TestAddons'))

        self.assertRaises(TypeError, self.addon_manager.set_addon_dirs, new_addon_dir)

    def test_get_addon_count_after_1(self):
        """
        setting addon search directory explicitly and in right way
        """
        new_addon_dir = os.path.abspath(os.path.join('.', 'TestAddons'))
        self.addon_manager.set_addon_dirs([new_addon_dir])
        self.addon_manager.load_addons()

        expected = 1
        actual = len(self.addon_manager.get_loaded_addons(type_filter='*'))
        self.assertEqual(expected, actual, "only 1 addon should be found")


if __name__ == '__main__':
    unittest.main()
