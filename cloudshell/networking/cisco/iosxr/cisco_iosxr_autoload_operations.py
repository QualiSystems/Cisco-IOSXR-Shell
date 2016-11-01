from cloudshell.networking.cisco.autoload.cisco_generic_snmp_autoload import CiscoGenericSNMPAutoload


class CiscoIOSXRSNMPAutoload(CiscoGenericSNMPAutoload):
    def __init__(self, snmp_handler=None, logger=None, supported_os=None):
        """Basic init with injected snmp handler and logger

        :param snmp_handler:
        :param logger:
        :return:
        """

        CiscoGenericSNMPAutoload.__init__(self, snmp_handler, logger, supported_os)

    def _get_power_supply_parent_id(self, port):
        parent_id = int(self.entity_table[port]['entPhysicalContainedIn'])
        result = ''
        if parent_id in self.entity_table.keys() and 'entPhysicalClass' in self.entity_table[parent_id]:
            if self.entity_table[parent_id]['entPhysicalClass'] == 'container':
                result = (self._get_power_supply_parent_id(parent_id) +
                          self.entity_table[parent_id]['entPhysicalParentRelPos'])
        return result

    def _get_ports_attributes(self):
        """Get resource details and attributes for every port in self.port_list

        :return:
        """

        self.logger.info('Load Ports:')
        for port in self.port_list:
            if_table_port_attr = {'ifType': 'str', 'ifPhysAddress': 'str', 'ifMtu': 'int', 'ifHighSpeed': 'int'}
            if_table = self.if_table[self.port_mapping[port]].copy()
            if_table.update(self.snmp.get_properties('IF-MIB', self.port_mapping[port], if_table_port_attr))
            interface_name = self.if_table[self.port_mapping[port]][self.IF_ENTITY].replace("'", '')
            if interface_name == '':
                interface_name = self.entity_table[port]['entPhysicalName']
            if interface_name == '':
                continue
            interface_type = if_table[self.port_mapping[port]]['ifType'].replace('/', '').replace("'", '')
            attribute_map = {'l2_protocol_type': interface_type,
                             'mac': if_table[self.port_mapping[port]]['ifPhysAddress'],
                             'mtu': if_table[self.port_mapping[port]]['ifMtu'],
                             'bandwidth': if_table[self.port_mapping[port]]['ifHighSpeed'],
                             'description': self.snmp.get_property('IF-MIB', 'ifAlias', self.port_mapping[port]),
                             'adjacent': self._get_adjacent(self.port_mapping[port])}
            attribute_map.update(self._get_interface_details(self.port_mapping[port]))
            attribute_map.update(self._get_ip_interface_details(self.port_mapping[port]))
            port_object = Port(name=interface_name, relative_path=self.relative_path[port], **attribute_map)
            self._add_resource(port_object)
            self.logger.info('Added ' + interface_name + ' Port')
        self.logger.info('Load port completed.')
