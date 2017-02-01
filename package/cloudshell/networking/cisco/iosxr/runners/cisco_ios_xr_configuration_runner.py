from cloudshell.networking.cisco.iosxr.cisco_ios_xr_cli_handler import CiscoIOSXRCliHandler
from cloudshell.networking.cisco.iosxr.flows.cisco_ios_xr_restore_flow import CiscoIOSXRRestoreFlow
from cloudshell.networking.cisco.runners.cisco_configuration_runner import CiscoConfigurationRunner


class CiscoIOSXRConfigurationRunner(CiscoConfigurationRunner):
    def __init__(self, cli, logger, context, api):
        super(CiscoIOSXRConfigurationRunner, self).__init__(cli, logger, context, api)
        self._cli_handler = CiscoIOSXRCliHandler(cli, context, logger, api)
        self._restore_flow = CiscoIOSXRRestoreFlow(self._cli_handler, self._logger)
        self.file_system = "bootflash:"
