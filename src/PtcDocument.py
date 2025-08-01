from src.PtcItem import ItemIdNotNumeric, PtcItem, PtcField

DOCUMENT_TYPE_REQUIREMENT   = 'Requirement Document'
DOCUMENT_TYPE_INTERFACE     = 'Interface Document'
DOCUMENT_TYPE_SPECIFICATION = 'Specification Document'

CONTENT_TYPE_REQUIREMENT   = 'Requirement'
CONTENT_TYPE_INTERFACE     = 'Interface'
CONTENT_TYPE_SPECIFICATION = 'Specification'

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
                    if item.category.value == 'Heading':
                        self.find_all_elements(item,element_list)

class Content(PtcItem):
    def __init__(self, content_id: int | str) -> None:
        super().__init__(content_id)
        self.fields.update(
            {
                # Properties
                'Category': PtcField('Category'),
                'Document ID': PtcField('Document ID'),
                # Details
                'Priority': PtcField('Priority'),
                'Item Owner': PtcField('Item Owner'),
                'Assigned Team': PtcField('Assigned Team'),
                'Functional Safety Classification': PtcField('Functional Safety Classification'),
                'Product Cybersecurity Relevance': PtcField('Product Cybersecurity Relevance'),
                'VnV Category': PtcField('VnV Category'),
                'Implementation Status': PtcField('Implementation Status'),
                'Source': PtcField('Source'),
                'Component': PtcField('Component'),
                'Function': PtcField('Function'),
                'Feature': PtcField('Feature'),
                'Variant': PtcField('Variant'),
                # Traces
                'Decomposed From': PtcField('Decomposed From'),
                'Decomposes To': PtcField('Decomposes To'),
                'Satisfied By': PtcField('Satisfied By'),
                'Modelled By': PtcField('Modelled By'),
                'Verified By': PtcField('Verified By'),
                'Validated By': PtcField('Validated By'),
                'Is Related To': PtcField('Is Related To'),
                'Implementing Source': PtcField('Implementing Source'),
                # Relationships
                'Contained By': PtcField('Contained By'),
                'Contains': PtcField('Contains'),
                'Changes Authorized By': PtcField('Changes Authorized By'),
                'Requirement belongs to Delivery': PtcField('Requirement belongs to Delivery'),
                'Spawns': PtcField('Spawns'),
                # Attachments
                'Source Link': PtcField('Source Link'),
                # Advanced
                'Trace Count': PtcField('Trace Count'),
                'Downstream Trace Count': PtcField('Downstream Trace Count'),
                'Upstream Trace Count': PtcField('Upstream Trace Count'),
                'Validated By Trace Count': PtcField('Validated By Trace Count'),
                'Item Maturity Level': PtcField('Item Maturity Level'),
                # Comments
                'VnV Comment': PtcField('VnV Comment'),
                # History
                'Modified By': PtcField('Modified By'),
                'Created By': PtcField('Created By')

            }
        )
        self.update_fields()

    # Properties
    @property
    def category(self) -> PtcField:
        return self._fields['Category']

    @category.setter
    def category(self, value: str) -> None:
        self._fields['Category'].value = value

    @property
    def document_id(self) -> PtcField:
        return self._fields['Document ID']

    @document_id.setter
    def document_id(self, value: str) -> None:
        self._fields['Document ID'].value = value

    #Details
    @property
    def priority(self) -> PtcField:
        return self._fields['Priority']

    @priority.setter
    def priority(self, value: str) -> None:
        self._fields['Priority'].value = value

    @property
    def item_owner(self) -> PtcField:
        return self._fields['Item Owner']

    @item_owner.setter
    def item_owner(self, value: str) -> None:
        self._fields['Item Owner'].value = value

    @property
    def assigned_team(self) -> PtcField:
        return self._fields['Assigned Team']

    @assigned_team.setter
    def assigned_team(self, value: str) -> None:
        self._fields['Assigned Team'].value = value

    @property
    def functional_safety_classification(self) -> PtcField:
        return self._fields['Functional Safety Classification']

    @functional_safety_classification.setter
    def functional_safety_classification(self, value: str) -> None:
        self._fields['Functional Safety Classification'].value = value

    @property
    def product_cybersecurity_classification(self) -> PtcField:
        return self._fields['Product Cybersecurity Relevance']

    @product_cybersecurity_classification.setter
    def product_cybersecurity_classification(self, value: str) -> None:
        self._fields['Product Cybersecurity Relevance'].value = value

    @property
    def vnv_category(self) -> PtcField:
        return self._fields['VnV Category']

    @vnv_category.setter
    def vnv_category(self, value: str) -> None:
        self._fields['VnV Category'].value = value

    @property
    def implementation_status(self) -> PtcField:
        return self._fields['Implementation Status']

    @implementation_status.setter
    def implementation_status(self, value: str) -> None:
        self._fields['Implementation Status'].value = value

    @property
    def source(self) -> PtcField:
        return self._fields['Source']

    @source.setter
    def source(self, value: str) -> None:
        self._fields['Source'].value = value

    @property
    def component(self) -> PtcField:
        return self._fields['Component']

    @component.setter
    def component(self, value: str) -> None:
        self._fields['Component'].value = value

    @property
    def function(self) -> PtcField:
        return self._fields['Function']

    @function.setter
    def function(self, value: str) -> None:
        self._fields['Function'].value = value

    @property
    def feature(self) -> PtcField:
        return self._fields['Feature']

    @feature.setter
    def feature(self, value: str) -> None:
        self._fields['Feature'].value = value

    @property
    def variant(self) -> PtcField:
        return self._fields['Variant']

    @variant.setter
    def variant(self, value: str) -> None:
        self._fields['Variant'].value = value


    #Traces
    @property
    def decomposed_from(self) -> PtcField:
        return self._fields['Decomposed From']

    @decomposed_from.setter
    def decomposed_from(self, value: str) -> None:
        self._fields['Decomposed From'].value = value

    @property
    def decomposes_to(self) -> PtcField:
        return self._fields['Decomposed From']

    @decomposes_to.setter
    def decomposes_to(self, value: str) -> None:
        self._fields['Decomposes To'].value = value

    @property
    def satisfied_by(self) -> PtcField:
        return self._fields['Satisfied By']

    @satisfied_by.setter
    def satisfied_by(self, value: str) -> None:
        self._fields['Satisfied By'].value = value

    @property
    def modelled_by(self) -> PtcField:
        return self._fields['Modelled By']

    @modelled_by.setter
    def modelled_by(self, value: str) -> None:
        self._fields['Modelled By'].value = value

    @property
    def verified_by(self) -> PtcField:
        return self._fields['Verified By']

    @verified_by.setter
    def verified_by(self, value: str) -> None:
        self._fields['Verified By'].value = value

    @property
    def validated_by(self) -> PtcField:
        return self._fields['Validated By']

    @validated_by.setter
    def validated_by(self, value: str) -> None:
        self._fields['Validated By'].value = value

    @property
    def is_related_to(self) -> PtcField:
        return self._fields['Is Related To']

    @is_related_to.setter
    def is_related_to(self, value: str) -> None:
        self._fields['Is Related To'].value = value

    @property
    def implementing_source(self) -> PtcField:
        return self._fields['Implementing Source']

    @implementing_source.setter
    def implementing_source(self, value: str) -> None:
        self._fields['Implementing Source'].value = value

    #Relationships
    @property
    def contained_by(self) -> PtcField:
        return self._fields['Contained By']

    @contained_by.setter
    def contained_by(self, value: str) -> None:
        self._fields['Contained By'].value = value

    @property
    def contains(self) -> PtcField:
        return self._fields['Contains']

    @contains.setter
    def contains(self, value: str) -> None:
        self._fields['Contains'].value = value

    @property
    def changes_authorized_by(self) -> PtcField:
        return self._fields['Changes Authorized By']

    @changes_authorized_by.setter
    def changes_authorized_by(self, value: str) -> None:
        self._fields['Changes Authorized By'].value = value

    @property
    def requirement_belongs_to_delivery(self) -> PtcField:
        return self._fields['Requirement belongs to Delivery']

    @requirement_belongs_to_delivery.setter
    def requirement_belongs_to_delivery(self, value: str) -> None:
        self._fields['Requirement belongs to Delivery'].value = value

    @property
    def spawns(self) -> PtcField:
        return self._fields['Spawns']

    @spawns.setter
    def spawns(self, value: str) -> None:
        self._fields['Spawns'].value = value


    #Attachments
    @property
    def source_link(self) -> PtcField:
        return self._fields['Source Link']

    @source_link.setter
    def source_link(self, value: str) -> None:
        self._fields['Source Link'].value = value

    #Advanced
    @property
    def trace_count(self) -> PtcField:
        return self._fields['Trace Count']

    @trace_count.setter
    def trace_count(self, value: str) -> None:
        self._fields['Trace Count'].value = value

    @property
    def downstream_trace_count(self) -> PtcField:
        return self._fields['Downstream Trace Count']

    @downstream_trace_count.setter
    def downstream_trace_count(self, value: str) -> None:
        self._fields['Downstream Trace Count'].value = value

    @property
    def upstream_trace_count(self) -> PtcField:
        return self._fields['Upstream Trace Count']

    @upstream_trace_count.setter
    def upstream_trace_count(self, value: str) -> None:
        self._fields['Upstream Trace Count'].value = value

    @property
    def validated_by_trace_count(self) -> PtcField:
        return self._fields['Validated By Trace Count']

    @validated_by_trace_count.setter
    def validated_by_trace_count(self, value: str) -> None:
        self._fields['Validated By Trace Count'].value = value

    @property
    def item_maturity_level(self) -> PtcField:
        return self._fields['Item Maturity Level']

    @item_maturity_level.setter
    def item_maturity_level(self, value: str) -> None:
        self._fields['Item Maturity Level'].value = value

    # Comments
    @property
    def vnv_comment(self) -> PtcField:
        return self._fields['VnV Comment']

    @vnv_comment.setter
    def vnv_comment(self, value: str) -> None:
        self._fields['VnV Comment'].value = value

    #History
    @property
    def modified_by(self) -> PtcField:
        return self._fields['Modified By']

    @modified_by.setter
    def modified_by(self, value: str) -> None:
        self._fields['Modified By'].value = value

    @property
    def created_by(self) -> PtcField:
        return self._fields['Created By']

    @created_by.setter
    def created_by(self, value: str) -> None:
        self._fields['Created By'].value = value


class Requirement(Content):
    def __init__(self, content_id: str) -> None:
        super().__init__(content_id)
        self.fields.update(
            {
                # Details
                'Text': PtcField('Text'),
                'Keywords': PtcField('Keywords'),
                'Risk': PtcField('Risk'),
                'Risk Comment': PtcField('Risk Comment'),
                'Regulatory Relevance': PtcField('Regulatory Relevance'),
                'Requirement Category': PtcField('Requirement Category'),
                # Traces
                'Details': PtcField('Details'),
                'Requires': PtcField('Requires'),
                'Provides': PtcField('Provides'),
            }
        )
        super().update_fields()
        self.text.value = self.item_report_raw.split('Text')[1].removeprefix(': ')

    # Details
    @property
    def text(self) -> PtcField:
        return self._fields['Text']

    @text.setter
    def text(self, value: str) -> None:
        self._fields['Text'].value = value

    @property
    def keywords(self) -> PtcField:
        return self._fields['Keywords']

    @keywords.setter
    def keywords(self, value: str) -> None:
        self._fields['Keywords'].value = value

    @property
    def risk(self) -> PtcField:
        return self._fields['Risk']

    @risk.setter
    def risk(self, value: str) -> None:
        self._fields['Risk'].value = value

    @property
    def risk_comment(self) -> PtcField:
        return self._fields['Risk Comment']

    @risk_comment.setter
    def risk_comment(self, value: str) -> None:
        self._fields['Risk Comment'].value = value

    @property
    def regulatory_relevance(self) -> PtcField:
        return self._fields['Regulatory Relevance']

    @regulatory_relevance.setter
    def regulatory_relevance(self, value: str) -> None:
        self._fields['Regulatory Relevance'].value = value

    @property
    def requirement_category(self) -> PtcField:
        return self._fields['Requirement Category']

    @requirement_category.setter
    def requirement_category(self, value: str) -> None:
        self._fields['Requirement Category'].value = value

    # Traces
    @property
    def details(self) -> PtcField:
        return self._fields['Details']

    @details.setter
    def details(self, value: str) -> None:
        self._fields['Details'].value = value

    @property
    def requires(self) -> PtcField:
        return self._fields['Requires']

    @requires.setter
    def requires(self, value: str) -> None:
        self._fields['Requires'].value = value

    @property
    def provides(self) -> PtcField:
        return self._fields['Provides']

    @provides.setter
    def provides(self, value: str) -> None:
        self._fields['Provides'].value = value

class Interface(Content):
    def __init__(self, content_id: str):
        super().__init__(content_id)
        self.fields.update(
            {
                # Signal Properties
                'Interface Class': PtcField('Interface Class'),
                'Interface Name': PtcField('Interface Name'),
                'Minimum': PtcField('Minimum'),
                'Maximum': PtcField('Maximum'),
                'Offset': PtcField('Offset'),
                'Resolution': PtcField('Resolution'),
                'Initial Value': PtcField('Initial Value'),
                'Unit': PtcField('Unit'),
                'Signal Dimension': PtcField('Signal Dimension'),
                'Data Type': PtcField('Data Type'),
                'Error Value': PtcField('Error Value'),
                'Value Type': PtcField('Value Type'),
                'Factor': PtcField('Factor'),
                'Enum Value': PtcField('Enum Value'),
                'Enum Value Symbol': PtcField('Enum Value Symbol'),
                'Enum Value List': PtcField('Enum Value List'),
                'Enum Value Symbol List': PtcField('Enum Value Symbol List'),
                'Enum Value Description': PtcField('Enum Value Description'),
                # AUTOSAR Properties
                'Data Element Name': PtcField('Data Element Name'),
                'Sender SWC': PtcField('Sender SWC'),
                'Receiver SWCs': PtcField('Receiver SWCs'),
                'Sender Runnable': PtcField('Sender Runnable'),
                'Receiver Runnables': PtcField('Receiver Runnables'),
                'Sender Ports': PtcField('Sender Ports'),
                'Receiver Ports': PtcField('Receiver Ports'),
                'Port Interfaces': PtcField('Port Interfaces'),
                # Bus Description
                'Sender': PtcField('Sender'),
                'Receiver': PtcField('Receiver'),
                'Sending Cycle Time': PtcField('Sending Cycle Time'),
                'Message Name': PtcField('Message Name'),
                'Timeout Duration': PtcField('Timeout Duration'),
                'Interface Type': PtcField('Interface Type'),
                'Bus': PtcField('Bus'),
                'CAN message ID': PtcField('CAN message ID'),
                'Signal Startposition': PtcField('Signal Startposition'),
                'Signal Length': PtcField('Signal Length'),
                'Timeout Substitute Value': PtcField('Timeout Substitute Value'),
                'Timeout Inheritance Value': PtcField('Timeout Inheritance Value'),
                # Traces
                'Satisfies': PtcField('Satisfies'),
                'Required By': PtcField('Required By'),
                'Provided By': PtcField('Provided By'),
            }
        )
        self.update_fields()

    # Signal Properties
    @property
    def interface_class(self) -> PtcField:
        return self._fields['Interface Class']

    @interface_class.setter
    def interface_class(self, value: str) -> None:
        self._fields['Interface Class'].value = value

    @property
    def interface_name(self) -> PtcField:
        return self._fields['Interface Name']

    @interface_name.setter
    def interface_name(self, value: str) -> None:
        self._fields['Interface Name'].value = value

    @property
    def minimum(self) -> PtcField:
        return self._fields['Minimum']

    @minimum.setter
    def minimum(self, value: str) -> None:
        self._fields['Minimum'].value = value

    @property
    def maximum(self) -> PtcField:
        return self._fields['Maximum']

    @maximum.setter
    def maximum(self, value: str) -> None:
        self._fields['Maximum'].value = value

    @property
    def offset(self) -> PtcField:
        return self._fields['Offset']

    @offset.setter
    def offset(self, value: str) -> None:
        self._fields['Offset'].value = value

    @property
    def resolution(self) -> PtcField:
        return self._fields['Resolution']

    @resolution.setter
    def resolution(self, value: str) -> None:
        self._fields['Resolution'].value = value

    @property
    def initial_value(self) -> PtcField:
        return self._fields['Initial Value']

    @initial_value.setter
    def initial_value(self, value: str) -> None:
        self._fields['Initial Value'].value = value

    @property
    def unit(self) -> PtcField:
        return self._fields['Unit']

    @unit.setter
    def unit(self, value: str) -> None:
        self._fields['Unit'].value = value

    @property
    def signal_dimension(self) -> PtcField:
        return self._fields['Signal Dimension']

    @signal_dimension.setter
    def signal_dimension(self, value: str) -> None:
        self._fields['Signal Dimension'].value = value

    @property
    def data_type(self) -> PtcField:
        return self._fields['Data Type']

    @data_type.setter
    def data_type(self, value: str) -> None:
        self._fields['Data Type'].value = value

    @property
    def error_value(self) -> PtcField:
        return self._fields['Error Value']

    @error_value.setter
    def error_value(self, value: str) -> None:
        self._fields['Error Value'].value = value

    @property
    def value_type(self) -> PtcField:
        return self._fields['Value Type']

    @value_type.setter
    def value_type(self, value: str) -> None:
        self._fields['Value Type'].value = value

    @property
    def factor(self) -> PtcField:
        return self._fields['Factor']

    @factor.setter
    def factor(self, value: str) -> None:
        self._fields['Factor'].value = value

    @property
    def enum_value(self) -> PtcField:
        return self._fields['Enum Value']

    @enum_value.setter
    def enum_value(self, value: str) -> None:
        self._fields['Enum Value'].value = value

    @property
    def enum_value_symbol(self) -> PtcField:
        return self._fields['Enum Value Symbol']

    @enum_value_symbol.setter
    def enum_value_symbol(self, value: str) -> None:
        self._fields['Enum Value Symbol'].value = value

    @property
    def enum_value_list(self) -> PtcField:
        return self._fields['Enum Value List']

    @enum_value_list.setter
    def enum_value_list(self, value: str) -> None:
        self._fields['Enum Value List'].value = value

    @property
    def enum_value_symbol_list(self) -> PtcField:
        return self._fields['Enum Value Symbol List']

    @enum_value_symbol_list.setter
    def enum_value_symbol_list(self, value: str) -> None:
        self._fields['Enum Value Symbol List'].value = value

    @property
    def enum_value_description(self) -> PtcField:
        return self._fields['Enum Value Description']

    @enum_value_description.setter
    def enum_value_description(self, value: str) -> None:
        self._fields['Enum Value Description'].value = value


    #AUTOSAR Properties
    @property
    def data_element_name(self) -> PtcField:
        return self._fields['Data Element Name']

    @data_element_name.setter
    def data_element_name(self, value: str) -> None:
        self._fields['Data Element Name'].value = value

    @property
    def sender_swc(self) -> PtcField:
        return self._fields['Sender SWC']

    @sender_swc.setter
    def sender_swc(self, value: str) -> None:
        self._fields['Sender SWC'].value = value

    @property
    def receiver_swcs(self) -> PtcField:
        return self._fields['Receiver SWCs']

    @receiver_swcs.setter
    def receiver_swcs(self, value: str) -> None:
        self._fields['Receiver SWCs'].value = value

    @property
    def sender_runnable(self) -> PtcField:
        return self._fields['Sender Runnable']

    @sender_runnable.setter
    def sender_runnable(self, value: str) -> None:
        self._fields['Sender Runnable'].value = value

    @property
    def receiver_runnables(self) -> PtcField:
        return self._fields['Receiver Runnables']

    @receiver_runnables.setter
    def receiver_runnables(self, value: str) -> None:
        self._fields['Receiver Runnables'].value = value

    @property
    def sender_ports(self) -> PtcField:
        return self._fields['Sender Ports']

    @sender_ports.setter
    def sender_ports(self, value: str) -> None:
        self._fields['Sender Ports'].value = value

    @property
    def receiver_ports(self) -> PtcField:
        return self._fields['Receiver Ports']

    @receiver_ports.setter
    def receiver_ports(self, value: str) -> None:
        self._fields['Receiver Ports'].value = value

    @property
    def port_interfaces(self) -> PtcField:
        return self._fields['Port Interfaces']

    @port_interfaces.setter
    def port_interfaces(self, value: str) -> None:
        self._fields['Port Interfaces'].value = value

    #Bus Description
    @property
    def sender(self) -> PtcField:
        return self._fields['Sender']

    @sender.setter
    def sender(self, value: str) -> None:
        self._fields['Sender'].value = value

    @property
    def receiver(self) -> PtcField:
        return self._fields['Receiver']

    @receiver.setter
    def receiver(self, value: str) -> None:
        self._fields['Receiver'].value = value

    @property
    def sending_cycle_time(self) -> PtcField:
        return self._fields['Sending Cycle Time']

    @sending_cycle_time.setter
    def sending_cycle_time(self, value: str) -> None:
        self._fields['Sending Cycle Time'].value = value

    @property
    def message_name(self) -> PtcField:
        return self._fields['Message Name']

    @message_name.setter
    def message_name(self, value: str) -> None:
        self._fields['Message Name'].value = value

    @property
    def timeout_duration(self) -> PtcField:
        return self._fields['Timeout Duration']

    @timeout_duration.setter
    def timeout_duration(self, value: str) -> None:
        self._fields['Timeout Duration'].value = value

    @property
    def interface_type(self) -> PtcField:
        return self._fields['Interface Type']

    @interface_type.setter
    def interface_type(self, value: str) -> None:
        self._fields['Interface Type'].value = value

    @property
    def bus(self) -> PtcField:
        return self._fields['Bus']

    @bus.setter
    def bus(self, value: str) -> None:
        self._fields['Bus'].value = value

    @property
    def can_message_id(self) -> PtcField:
        return self._fields['CAN message ID']

    @can_message_id.setter
    def can_message_id(self, value: str) -> None:
        self._fields['CAN message ID'].value = value

    @property
    def signal_startposition(self) -> PtcField:
        return self._fields['Signal Startposition']

    @signal_startposition.setter
    def signal_startposition(self, value: str) -> None:
        self._fields['Signal Startposition'].value = value

    @property
    def signal_length(self) -> PtcField:
        return self._fields['Signal Length']

    @signal_length.setter
    def signal_length(self, value: str) -> None:
        self._fields['Signal Length'].value = value

    @property
    def timeout_substitute_value(self) -> PtcField:
        return self._fields['Timeout Substitute Value']

    @timeout_substitute_value.setter
    def timeout_substitute_value(self, value: str) -> None:
        self._fields['Timeout Substitute Value'].value = value

    @property
    def timeout_inheritance_value(self) -> PtcField:
        return self._fields['Timeout Inheritance Value']

    @timeout_inheritance_value.setter
    def timeout_inheritance_value(self, value: str) -> None:
        self._fields['Timeout Inheritance Value'].value = value

    # Traces
    @property
    def satisfies(self) -> PtcField:
        return self._fields['Satisfies']

    @satisfies.setter
    def satisfies(self, value: str) -> None:
        self._fields['Satisfies'].value = value

    @property
    def required_by(self) -> PtcField:
        return self._fields['Required By']

    @required_by.setter
    def required_by(self, value: str) -> None:
        self._fields['Required By'].value = value

    @property
    def provided_by(self) -> PtcField:
        return self._fields['Provided By']

    @provided_by.setter
    def provided_by(self, value: str) -> None:
        self._fields['Provided By'].value = value

    def set_text(self):
        pass

    @staticmethod
    def update_interface(list_of_interfaces, **kwargs):
        """ Update fields for Interfaces
        list_of_interfaces: List of interface items
        """
        if len(kwargs):
            for interface in list_of_interfaces:
                if interface.category.value == 'Interface':
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