from cloudshell.cli.command_mode_helper import CommandModeHelper
from cloudshell.networking.cisco.cisco_cli_handler import CiscoCliHandler
from cloudshell.networking.cisco.cisco_command_modes import EnableCommandMode, DefaultCommandMode, ConfigCommandMode


class CiscoIOSXRCliHandler(CiscoCliHandler):
    def __init__(self, cli, context, logger, api):
        super(CiscoIOSXRCliHandler, self).__init__(cli, context, logger, api)
        modes = CommandModeHelper.create_command_mode(context)
        self.default_mode = modes[DefaultCommandMode]
        self.enable_mode = modes[EnableCommandMode]
        self.config_mode = modes[ConfigIOSXRCommandMode]

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

class ConfigIOSXRCommandMode(CommandMode):
    PROMPT = r'\(config.*\)#\s*$'
    ENTER_COMMAND = 'configure terminal'
    EXIT_COMMAND = 'exit'

    def __init__(self, context):
        """
        Initialize Config command mode

        :param context:
        """
        exit_action_map = {
            self.PROMPT: lambda session, logger: session.send_line('exit', logger),
            'commit.*[\[\(][Yy]es/[Nn]o.*[\)\]]': lambda session, logger: session.send_line('yes', logger)}
        CommandMode.__init__(self, ConfigCommandMode.PROMPT,
                             ConfigCommandMode.ENTER_COMMAND,
                             ConfigCommandMode.EXIT_COMMAND,
                             exit_action_map=exit_action_map)

CommandMode.RELATIONS_DICT = {
    DefaultCommandMode: {
        EnableCommandMode: {
            ConfigIOSXRCommandMode: {}
        }
    }
}
