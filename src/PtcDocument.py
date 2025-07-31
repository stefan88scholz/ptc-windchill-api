from src.PtcItem import ItemIdNotNumeric, PtcItem, PtcField

DOCUMENT_TYPE_REQUIREMENT   = 'Requirement Document'
DOCUMENT_TYPE_INTERFACE     = 'Interface Document'
DOCUMENT_TYPE_SPECIFICATION = 'Specification Document'

CONTENT_TYPE_REQUIREMENT   = 'Requirement'
CONTENT_TYPE_INTERFACE     = 'Interface'
CONTENT_TYPE_SPECIFICATION = 'Specification'

INTERFACE_CLASS_IN = 'In'
INTERFACE_CLASS_OUT = 'Out'
INTERFACE_CLASS_NA = 'n.a.'
INTERFACE_CLASS_TBD = 't.b.d.'
INTERFACE_CLASS_SIGNAL = 'Signal'
INTERFACE_CLASS_NVDATA = 'NvData'

class PtcDocument(PtcItem):
    """ Attributes and Methods of PTC Windchill items"""

    def __init__(self, document_id: str):
        super().__init__(document_id)

        self.document_short_title: PtcField = PtcField('Document Short Title')
        self.fields.append(self.document_short_title)

        self.contains: PtcField = PtcField('Contains')
        self.fields.append(self.contains)

        self.update_fields()

        self.elements = list()
        content = self.contains.value.replace(' ', '')
        content = content.replace('ay', '').split(',')
        for element in content:
            item = self.get_item(element)
            print(item.text.value)
            self.elements.append(item)
            self.find_all_elements(item,self.elements)

    def get_item(self, element):
        item = None
        if self.type.value == DOCUMENT_TYPE_REQUIREMENT:
            item = Requirement(element)
        elif self.type.value == DOCUMENT_TYPE_SPECIFICATION:
            pass
        elif self.type.value == DOCUMENT_TYPE_INTERFACE:
            item = Interface(element)
        return item

    def find_all_elements(self, item, element_list):
        if isinstance(item,Content):
            if item.contains.value:
                content = item.contains.value.replace(' ', '')
                content = content.replace('ay', '').split(',')
                for element in content:
                    if not isinstance(element, int) and (isinstance(element, str) and not element.isnumeric()):
                        raise ItemIdNotNumeric(f'Item with ID {element} is not numeric')
                    item = self.get_item(element)
                    print(ascii(item.text.value))
                    element_list.append(item)
                    if item.category.value == CATEGORY_HEADING:
                        self.find_all_elements(item,element_list)

class Content(PtcItem):

    def __init__(self, content_id: int | str) -> None:
        super().__init__(content_id)
        #Properties
        self.category: PtcField                             = PtcField('Category')
        self.fields.append(self.category)

        self.document_id: PtcField                          = PtcField('Document ID')
        self.fields.append(self.document_id)

        #Details
        self.priority: PtcField                             = PtcField('Priority')
        self.fields.append(self.priority)

        self.item_owner: PtcField                           = PtcField('Item Owner')
        self.fields.append(self.item_owner)

        self.assigned_team: PtcField                        = PtcField('Assigned Team')
        self.fields.append(self.assigned_team)

        self.functional_safety_classification: PtcField     = PtcField('Functional Safety Classification')
        self.fields.append(self.functional_safety_classification)

        self.product_cybersecurity_classification: PtcField = PtcField('Product Cybersecurity Relevance')
        self.fields.append(self.product_cybersecurity_classification)

        self.vnv_category: PtcField                         = PtcField('VnV Category')
        self.fields.append(self.vnv_category)

        self.implementation_status: PtcField                = PtcField('Implementation Status')
        self.fields.append(self.implementation_status)


        self.source: PtcField                               = PtcField('Source')
        self.fields.append(self.source)

        self.component: PtcField                            = PtcField('Component')
        self.fields.append(self.component)

        self.function: PtcField                             = PtcField('Function')
        self.fields.append(self.function)

        self.feature: PtcField                              = PtcField('Feature')
        self.fields.append(self.feature)

        self.variant: PtcField                              = PtcField('Variant')
        self.fields.append(self.variant)

        #Traces
        self.decomposed_from: PtcField                      = PtcField('Decomposed From')
        self.fields.append(self.decomposed_from)

        self.decomposes_to: PtcField                        = PtcField('Decomposes To')
        self.fields.append(self.decomposes_to)

        self.satisfied_by: PtcField                         = PtcField('Satisfied By')
        self.fields.append(self.satisfied_by)

        self.modelled_by: PtcField                          = PtcField('Modelled By')
        self.fields.append(self.modelled_by)

        self.verified_by: PtcField                          = PtcField('Verified By')
        self.fields.append(self.verified_by)

        self.validated_by: PtcField                         = PtcField('Validated By')
        self.fields.append(self.validated_by)

        self.is_related_to: PtcField                        = PtcField('Is Related To')
        self.fields.append(self.is_related_to)

        self.is_related_to_apostrophe: PtcField             = PtcField('Is Related To\'')
        self.fields.append(self.is_related_to_apostrophe)

        self.implementing_source: PtcField                  = PtcField('Implementing Source')
        self.fields.append(self.implementing_source)

        #Relationships
        self.contained_by: PtcField                         = PtcField('Contained By')
        self.fields.append(self.contained_by)

        self.contains: PtcField                             = PtcField('Contains')
        self.fields.append(self.contains)

        self.changes_authorized_by: PtcField                = PtcField('Changes Authorized By')
        self.fields.append(self.changes_authorized_by)

        self.requirement_belongs_to_delivery: PtcField      = PtcField('Requirement belongs to Delivery')
        self.fields.append(self.requirement_belongs_to_delivery)

        self.spawns: PtcField                               = PtcField('Spawns')
        self.fields.append(self.spawns)

        #Attachments
        self.source_link: PtcField                          = PtcField('Source Link')
        self.fields.append(self.source_link)

        #Advanced
        self.trace_count: PtcField                          = PtcField('Trace Count')
        self.fields.append(self.trace_count)

        self.downstream_trace_count: PtcField               = PtcField('Downstream Trace Count')
        self.fields.append(self.downstream_trace_count)

        self.upstream_trace_count: PtcField                 = PtcField('Upstream Trace Count')
        self.fields.append(self.upstream_trace_count)

        self.validated_by_trace_count: PtcField             = PtcField('Validated By Trace Count')
        self.fields.append(self.validated_by_trace_count)

        self.item_maturity_level: PtcField                  = PtcField('Item Maturity Level')
        self.fields.append(self.item_maturity_level)

        #Comments
        self.vnv_comment: PtcField                          = PtcField('VnV Comment')
        self.fields.append(self.vnv_comment)

        #History
        self.modified_by: PtcField                          = PtcField('Modified By')
        self.fields.append(self.modified_by)

        self.created_by: PtcField                           = PtcField('Created By')
        self.fields.append(self.created_by)

        self.update_fields()

class Requirement(Content):
    def __init__(self, content_id: str) -> None:
        super().__init__(content_id)
        # Details
        self.text: PtcField                                 = PtcField('Text')
        self.fields.append(self.text)

        self.keywords: PtcField                             = PtcField('Keywords')
        self.fields.append(self.keywords)

        self.risk: PtcField                                 = PtcField('Risk')
        self.fields.append(self.risk)

        self.risk_comment: PtcField                         = PtcField('Risk Comment')
        self.fields.append(self.risk_comment)

        self.regulatory_relevance: PtcField                 = PtcField('Regulatory Relevance')
        self.fields.append(self.regulatory_relevance)

        self.requirement_category: PtcField                 = PtcField('Requirement Category')
        self.fields.append(self.requirement_category)

        # Traces
        self.details: PtcField                              = PtcField('Details')
        self.fields.append(self.details)

        self.requires: PtcField                             = PtcField('Requires')
        self.fields.append(self.requires)

        self.provides: PtcField                             = PtcField('Provides')
        self.fields.append(self.provides)

        super().update_fields()

        self.text.value = self.item_report_raw.split('Text')[1].removeprefix(': ')

class Interface(Content):
    def __init__(self, content_id: str):
        super().__init__(content_id)
        # Signal Properties
        self.interface_class = PtcField('Interface Class')
        self.fields.append(self.interface_class)

        self.interface_name = PtcField('Interface Name')
        self.fields.append(self.interface_name)

        self.minimum = PtcField('Minimum')
        self.fields.append(self.minimum)

        self.maximum = PtcField('Maximum')
        self.fields.append(self.maximum)

        self.offset = PtcField('Offset')
        self.fields.append(self.offset)

        self.resolution = PtcField('Resolution')
        self.fields.append(self.resolution)

        self.initial_value = PtcField('Initial Value')
        self.fields.append(self.initial_value)

        self.unit = PtcField('Unit')
        self.fields.append(self.unit)

        self.signal_dimension = PtcField('Signal Dimension')
        self.fields.append(self.signal_dimension)

        self.data_type = PtcField('Data Type')
        self.fields.append(self.data_type)

        self.dlc = PtcField('DLC')
        self.fields.append(self.dlc)

        self.error_value = PtcField('Error Value')
        self.fields.append(self.error_value)

        self.value_type = PtcField('Value Type')
        self.fields.append(self.value_type)

        self.factor = PtcField('Factor')
        self.fields.append(self.factor)

        self.enum_value = PtcField('Enum Value')
        self.fields.append(self.enum_value)

        self.enum_value_symbol = PtcField('Enum Value Symbol')
        self.fields.append(self.enum_value_symbol)

        self.enum_value_list = PtcField('Enum Value List')
        self.fields.append(self.enum_value_list)

        self.enum_value_symbol_list = PtcField('Enum Value Symbol List')
        self.fields.append(self.enum_value_symbol_list)

        self.enum_value_description = PtcField('Enum Value Description')
        self.fields.append(self.enum_value_description)

        #AUTOSAR Properties
        self.data_element_name = PtcField('Data Element Name')
        self.fields.append(self.data_element_name)

        self.sender_swc = PtcField('Sender SWC')
        self.fields.append(self.created_by)

        self.receiver_swcs = PtcField('Receiver SWCs')
        self.fields.append(self.receiver_swcs)

        self.sender_runnable = PtcField('Sender Runnable')
        self.fields.append(self.sender_runnable)

        self.receiver_runnables = PtcField('Receiver Runnables')
        self.fields.append(self.receiver_runnables)

        self.sender_ports = PtcField('Sender Ports')
        self.fields.append(self.sender_ports)

        self.receiver_ports = PtcField('Receiver Ports')
        self.fields.append(self.receiver_ports)

        self.port_interfaces = PtcField('Port Interfaces')
        self.fields.append(self.port_interfaces)

        #Bus Description
        self.sender = PtcField('Sender')
        self.fields.append(self.sender)

        self.receiver = PtcField('Receiver')
        self.fields.append(self.receiver)

        self.sending_cycle_time = PtcField('Sending Cycle Time')
        self.fields.append(self.sending_cycle_time)

        self.message_name = PtcField('Message Name')
        self.fields.append(self.message_name)

        self.timeout_duration = PtcField('Timeout Duration')
        self.fields.append(self.timeout_duration)

        self.interface_type = PtcField('Interface Type')
        self.fields.append(self.interface_type)

        self.bus = PtcField('Bus')
        self.fields.append(self.bus)

        self.can_message_id = PtcField('CAN message ID')
        self.fields.append(self.can_message_id)

        self.signal_startposition = PtcField('Signal Startposition')
        self.fields.append(self.signal_startposition)

        self.signal_length = PtcField('Signal Length')
        self.fields.append(self.signal_length)

        self.timeout_substitute_value = PtcField('Timeout Substitute Value')
        self.fields.append(self.timeout_substitute_value)

        self.timeout_inheritance_value = PtcField('Timeout Inheritance Value')
        self.fields.append(self.timeout_inheritance_value)

        # Traces
        self.satisfies = PtcField('Satisfies')
        self.fields.append(self.satisfies)

        self.required_by = PtcField('Required By')
        self.fields.append(self.required_by)

        self.provided_by = PtcField('Provided By')
        self.fields.append(self.provided_by)

        self.update_fields()

    def set_text(self):
        pass

    @staticmethod
    def update_interface(list_of_interfaces, **kwargs):
        """ Update fields for Interfaces
        list_of_interfaces: List of interface items
        """
        if len(kwargs):
            for interface in list_of_interfaces:
                if interface.category.value == CATEGORY_INTERFACE:
                    for key,value in kwargs.items():
                        switch = {
                            'state'                 : interface.state.name,
                            'component'             : interface.component.name,
                            'variant'               : interface.variant.name,
                            'cybersec'              : interface.product_cybersecurity_classification.name,
                            'interface_type'        : interface.interface_type.name,
                            'interface_class'       : interface.interface_class.name,
                            'sender_swc'            : interface.sender_swc.name,
                            'sender_ports'          : interface.sender_ports.name,
                            'receiver_swcs'         : interface.receiver_swcs.name,
                            'receiver_ports'        : interface.receiver_ports.name,
                            'data_element_name'     : interface.data_element_name.name,
                            'data_type'             : interface.data_type.name,
                            'signal_dimension'      : interface.signal_dimension.name,
                            'minimum'               : interface.minimum.name,
                            'maximum'               : interface.maximum.name,
                            'offset'                : interface.offset.name,
                            'initial_value'         : interface.initial_value.name,
                            'unit'                  : interface.unit.name,
                            'resolution'            : interface.resolution.name,
                            'enum_value_description': interface.enum_value_description.name,
                            'port_interfaces'       : interface.port_interfaces.name,
                            'interface_name'        : interface.interface_name.name,
                            'fusa'                  : interface.functional_safety_classification.name,
                            'vnv_category'          : interface.vnv_category.name,
                            'changes_auth_by'       : interface.changes_authorized_by.name,
                            'decomposed_from'       : interface.decomposed_from.name
                        }
                        if switch.get(key,'None') != 'None':
                            print(f'{key}: {value}')
                            interface.im_editissue(switch[key],value)