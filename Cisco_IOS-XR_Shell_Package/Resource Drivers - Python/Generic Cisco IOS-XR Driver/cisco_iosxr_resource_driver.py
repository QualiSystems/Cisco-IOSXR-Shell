import inject
from cloudshell.networking.cisco.cisco_connectivity_operations import CiscoConnectivityOperations
from cloudshell.networking.cisco.cisco_send_command_operations import CiscoSendCommandOperations
from cloudshell.networking.cisco.iosxr.cisco_iosxr_autoload_operations import CiscoIOSXRSNMPAutoload
from cloudshell.networking.cisco.iosxr.cisco_iosxr_configuration_operations import CiscoIOSXRConfigurationOperations

from cloudshell.networking.networking_resource_driver_interface import NetworkingResourceDriverInterface
from cloudshell.shell.core.context_utils import context_from_args
from cloudshell.shell.core.driver_bootstrap import DriverBootstrap
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.driver_utils import GlobalLock

import cloudshell.networking.cisco.iosxr.cisco_iosxr_configuration as driver_config


class CiscoIOSXRResourceDriver(ResourceDriverInterface, NetworkingResourceDriverInterface, GlobalLock):
    def __init__(self):
        super(CiscoIOSXRResourceDriver, self).__init__()
        bootstrap = DriverBootstrap()
        bootstrap.add_config(driver_config)
        bootstrap.initialize()

    @context_from_args
    def initialize(self, context):
        """Initialize method
        :type context: cloudshell.shell.core.context.driver_context.InitCommandContext
        """

        return 'Finished initializing'

    def cleanup(self):
        pass

    @context_from_args
    def ApplyConnectivityChanges(self, context, request):
        connectivity_operations = CiscoConnectivityOperations()
        connectivity_operations.logger.info('Start applying connectivity changes, request is: {0}'.format(str(request)))
        response = connectivity_operations.apply_connectivity_changes(request)
        connectivity_operations.logger.info('Finished applying connectivity changes, responce is: {0}'.format(str(
            response)))
        connectivity_operations.logger.info('Apply Connectivity changes completed')
        return response

    @GlobalLock.lock
    @context_from_args
    def restore(self, context, path, config_type, restore_method, vrf=None):
        """Restore selected file to the provided destination

        :param path: source config file
        :param config_type: running config
        :param restore_method: append or override methods
        """
        configuration_operations = CiscoIOSXRConfigurationOperations()
        response = configuration_operations.restore_configuration(source_file=path, restore_method=restore_method,
                                                                  config_type=config_type, vrf=vrf)
        configuration_operations.logger.info('Restore completed')
        configuration_operations.logger.info(response)

    @context_from_args
    def save(self, context, destination_host, source_filename, vrf=None):
        """Save selected file to the provided destination

        :param source_filename: source file, which will be saved
        :param destination_host: destination path where file will be saved
        """

        configuration_operations = CiscoIOSXRConfigurationOperations()
        response = configuration_operations.save_configuration(destination_host, source_filename, vrf)
        configuration_operations.logger.info('Save completed')
        return response

    @context_from_args
    def get_inventory(self, context):
        """Return device structure with all standard attributes

        :return: response
        :rtype: string
        """

        autoload_operations = CiscoIOSXRSNMPAutoload()
        response = autoload_operations.discover()
        autoload_operations.logger.info('Autoload completed')
        return response

    @GlobalLock.lock
    @context_from_args
    def update_firmware(self, context, remote_host, file_path):
        """Upload and updates firmware on the resource

        :param remote_host: path to tftp:// server where firmware file is stored
        :param file_path: firmware file name
        :return: result
        :rtype: string
        """

        firmware_operations = CiscoIOSXRConfigurationOperations()
        response = firmware_operations.update_firmware(remote_host=remote_host, file_path=file_path)
        firmware_operations.logger.info(response)

    @context_from_args
    def send_custom_command(self, context, command):
        """Send custom command

        :return: result
        :rtype: string
        """

        send_command_operations = CiscoSendCommandOperations()
        response = send_command_operations.send_command(command=command)

        return response

    @context_from_args
    def send_custom_config_command(self, context, command):
        """Send custom command in configuration mode

        :return: result
        :rtype: string
        """
        send_command_operations = CiscoSendCommandOperations()
        result_str = send_command_operations.send_config_command(command=command)
        return result_str

    @context_from_args
    def shutdown(self, context):
        pass
