from cloudshell.cli.command_mode_helper import CommandModeHelper
from cloudshell.networking.cisco.cisco_cli_handler import CiscoCliHandler
from cloudshell.networking.cisco.cisco_command_modes import EnableCommandMode, DefaultCommandMode, ConfigCommandMode


class CiscoIOSXRCliHandler(CiscoCliHandler):
    def __init__(self, cli, context, logger, api):
        super(CiscoIOSXRCliHandler, self).__init__(cli, context, logger, api)
        modes = CommandModeHelper.create_command_mode(context)
        self.default_mode = modes[DefaultCommandMode]
        self.enable_mode = modes[EnableCommandMode]
        self.config_mode = modes[ConfigCommandMode]

    def on_session_start(self, session, logger):
        """Send default commands to configure/clear session outputs
        :return:
        """

        self.enter_enable_mode(session=session, logger=logger)
        session.hardware_expect('terminal length 0', EnableCommandMode.PROMPT, logger)
        session.hardware_expect('terminal width 300', EnableCommandMode.PROMPT, logger)
        self._enter_config_mode(session, logger)
        session.hardware_expect('no logging console', ConfigCommandMode.PROMPT, logger)
        session.hardware_expect('commit', ConfigCommandMode.PROMPT, logger)
        session.hardware_expect('end', EnableCommandMode.PROMPT, logger)
