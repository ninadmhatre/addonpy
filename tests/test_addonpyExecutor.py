import unittest
from addonpy.addonpy import AddonLoader as loader
from addonpy.addonpyExecutor import AddonExecutor as runner
import sys


class TestAddonExecutor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        setup loader & runner with 2 addons instances
        """
        cls.run_mgr = runner(['start', 'execute'], ['stop'])
        cls.load_mgr = loader(verbose=False, recursive=True)
        cls.load_mgr.set_addon_dirs(['./data'])
        cls.load_mgr.load_addons()
        cls.cli_inst = cls.load_mgr.get_instance('CommandLineAddon')
        cls.fileio_inst = cls.load_mgr.get_instance('FileIOAddon')

    def test_by_config(self):
        # addon_executor = AddonExecutor(execute_order, stop_order)
        # self.assertEqual(expected, addon_executor.execute_with_config(addon))
        """
        test to check if runner can execute addon as per the execute and stop order mentioned in
        .info file.
        """

        self.run_mgr.by_default(self.cli_inst)
        output = self._get_lines_as_list(sys.stdout)

        self.assertTrue(output[0].startswith('Start'))
        self.assertTrue(output[1].startswith('Execute'))
        self.assertTrue(output[2].startswith('Stop'))

    def test_by_default(self):
        # addon_executor = AddonExecutor(execute_order, stop_order)
        # self.assertEqual(expected, addon_executor.execute_with_default(addon))
        """
        test to check if runner can execute addon as per initialization of runner. addon execution & stop order is not
        followed instead how runner is setup to run is used.
        """
        self.run_mgr.by_config(self.fileio_inst)

        output = self._get_lines_as_list(sys.stdout)

        self.assertTrue(output[0].startswith('Starting'))
        self.assertTrue(output[1].startswith('Executing'))
        self.assertTrue(output[2].startswith('Stopping'))

    def test_by_order(self):
        # addon_executor = AddonExecutor(execute_order, stop_order)
        # self.assertEqual(expected, addon_executor.execute_with_order(addon, execute_order, stop_order))
        """
        test to check if runner can execute addon as per order given as arguments.
        """
        self.run_mgr.by_order(self.cli_inst, ['execute', 'start'], ['stop'])
        output = self._get_lines_as_list(sys.stdout)

        self.assertTrue(output[0].startswith('Execute'))
        self.assertTrue(output[1].startswith('Start'))
        self.assertTrue(output[2].startswith('Stop'))

    def test_invalid_arguments(self):
        """
        test to check if runner raises exception when execution / stop order is not given as list
        """
        self.assertRaises(TypeError, self.run_mgr.by_order, 'start', 'stop')

    def _get_lines_as_list(self, input_string_io):
        output = input_string_io.getvalue().strip().split('\n')
        return output

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAddonExecutor)
    unittest.TextTestRunner(verbosity=2, buffer=True).run(suite)
