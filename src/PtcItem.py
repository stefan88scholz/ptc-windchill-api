import subprocess
from dataclasses import dataclass

class ItemIdNotNumeric(Exception):
    """ Exception raised if Item Id not numeric"""
    def __init__(self, message: str, error_code: str = '') -> None:
        super().__init__(message)
        self.message: str    = message
        self.error_code: str = error_code

    def __str__(self) -> str:
        return f'{self.message} (Error Code: {self.error_code})'

@dataclass()
class PtcField:
    _name: str
    _value: str = ''

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f'PtcItem({self.name}, {self.value})'


class PtcItem:
    """ Attributes and Methods of PTC Windchill items"""
    def __init__(self, item_id: int | str):
        if not isinstance(item_id,int) and (isinstance(item_id, str) and not item_id.isnumeric()):
            raise ItemIdNotNumeric(f'Item with ID {item_id} is not numeric')
        self._fields : dict[str, PtcField] = {
            'ID': PtcField('ID', item_id),
            'Type': PtcField('Type'),
            'Summary': PtcField('Summary'),
            'State': PtcField('State'),
            'Assigned User': PtcField('Assigned User')
        }
        self.item_report_raw: str  = ''

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value: dict[str, PtcField]) -> None:
        self._fields.update(value)

    @property
    def id(self) -> PtcField:
        return self._fields['ID']

    @id.setter
    def id(self, value: int | str) -> None:
        if not isinstance(value,int) and (isinstance(value, str) and not value.isnumeric()):
            raise ItemIdNotNumeric(f'ID {value} is not numeric')
        self._fields['ID'].value = value

    @property
    def type(self) -> PtcField:
        return self._fields['Type']

    @type.setter
    def type(self, value: str) -> None:
        self._fields['Type'].value = value

    @property
    def summary(self) -> PtcField:
        return self._fields['Summary']

    @summary.setter
    def summary(self, value: str) -> None:
        self._fields['Summary'].value = value

    @property
    def state(self) -> PtcField:
        return self._fields['State']

    @state.setter
    def state(self, value: str) -> None:
        self._fields['State'].value = value

    @property
    def assigned_user(self) -> PtcField:
        return self._fields['Assigned_user']

    @assigned_user.setter
    def assigned_user(self, value: str) -> None:
        self._fields['Assigned_user'].value = value


    def __str__(self) -> str:
        result: str = str()
        for field in self.fields.values():
            result = result + field.name + ': ' + field.value + '\n'
        return result

    def update_fields(self) -> None:
        for field in self.item_report():
            for i, (key,item) in enumerate(self._fields.items()):
                if field.startswith(key + ':'):
                    self._fields[key].value = field.replace(key + ': ', '')

    def remove_field_value(self, field_name: str, field_value: str):
        #print(f'im editissue --removeFieldValues=\'{field_name}={field_value}\' {self.item_id}')
        subprocess.run(f'im editissue --removeFieldValues=\'{field_name}={field_value}\' {self._fields['ID'].value}',
                       stdout=subprocess.PIPE)

    def add_field_value(self, field_name: str, field_value: str):
        #print(f'im editissue --addFieldValues=\'{field_name}={field_value}\' {self.item_id}')
        subprocess.run(f'im editissue --addFieldValues=\'{field_name}={field_value}\' {self._fields['ID'].value}',
                       stdout=subprocess.PIPE)

    def item_report(self):
        self.item_report_raw = self.im_viewissue().stdout.decode(errors='surrogateescape').__str__()
        return self.item_report_raw.split('\n')

    def im_editissue(self, field_name: str, field_value: str):
        """
        Edits and existing Windchill RV&S issue

        field_name
          specifies the field for the issue you want to change
        field_value
          specifies the field value for the issue

        """
        #print(f'im editissue --field=\'{field_name}={field_value}\' {self.item_id}')
        return subprocess.run(f'im editissue --field=\'{field_name}={field_value}\' {self._fields['ID'].value}')

    def im_viewissue(self):
        #print(f'im viewissue {self.item_id}')
        return subprocess.run(f'im viewissue {self._fields['ID'].value}', stdout=subprocess.PIPE)

class WorkItem(PtcItem):
    def __init__(self, work_item_id: int | str) -> None:
        super().__init__(work_item_id)
        self.fields.update(
            {
                'Component': PtcField('Component'),
                'Variant': PtcField('Variant'),
                'Contains Items': PtcField('Contains Items'),
                'Belongs To Work Item': PtcField('Belongs To Work Item')
            }
        )
        self.update_fields()

    @property
    def component(self) -> PtcField:
        return self._fields['Component']

    @component.setter
    def component(self, value: str) -> None:
        self._fields['Component'].value = value

    @property
    def variant(self) -> PtcField:
        return self._fields['Variant']

    @variant.setter
    def variant(self, value: str) -> None:
        self._fields['Variant'].value = value

    @property
    def contains_item(self) -> PtcField:
        return self._fields['Contains Items']

    @contains_item.setter
    def contains_item(self, value: str) -> None:
        self._fields['Contains Items'].value = value

    @property
    def belongs_to_work_item(self) -> PtcField:
        return self._fields['Belongs To Work Item']

    @belongs_to_work_item.setter
    def belongs_to_work_item(self, value: str) -> None:
        self._fields['Belongs To Work Item'].value = value

class Sprint(PtcItem):
    """Attributes and Methods of a PTC Windchill Sprint Item"""
    def __init__(self, sprint_id):
        super().__init__(sprint_id)
        self.fields.update(
            {
                'Responsible Team': PtcField('Responsible Team'),
                'Related Agile Product': PtcField('Related Agile Product'),
                'User Stories in Sprint': PtcField('User Stories in Sprint'),
                'Sprint Tested By': PtcField('Sprint Tested By'),
                'Tasks in Sprint': PtcField('Tasks in Sprint'),
                'Total Planned User Stories': PtcField('Total Planned User Stories'),
                'Total Planned Tasks': PtcField('Total Planned Tasks'),
                'Released In': PtcField('Released In'),
                'Total Remaining User Stories': PtcField('Total Remaining User Stories'),
                'Total Remaining Tasks': PtcField('Total Remaining Tasks'),
            }
        )

        self.update_fields()

    @property
    def responsible_team(self) -> PtcField:
        return self._fields['Responsible Team']

    @responsible_team.setter
    def responsible_team(self, value: str) -> None:
        self._fields['Responsible Team'].value = value

    @property
    def related_agile_product(self) -> PtcField:
        return self._fields['Related Agile Product']

    @related_agile_product.setter
    def related_agile_product(self, value: str) -> None:
        self._fields['Related Agile Product'].value = value

    @property
    def user_stories_in_sprint(self) -> PtcField:
        return self._fields['User Stories in Sprint']

    @user_stories_in_sprint.setter
    def user_stories_in_sprint(self, value: str) -> None:
        self._fields['User Stories in Sprint'].value = value

    @property
    def sprint_tested_by(self) -> PtcField:
        return self._fields['Sprint Tested By']

    @sprint_tested_by.setter
    def sprint_tested_by(self, value: str) -> None:
        self._fields['Sprint Tested By'].value = value

    @property
    def tasks_in_sprint(self) -> PtcField:
        return self._fields['Tasks in Sprint']

    @tasks_in_sprint.setter
    def tasks_in_sprint(self, value: str) -> None:
        self._fields['Tasks in Sprint'].value = value

    @property
    def total_planned_user_stories(self) -> PtcField:
        return self._fields['Total Planned User Stories']

    @total_planned_user_stories.setter
    def total_planned_user_stories(self, value: str) -> None:
        self._fields['Total Planned User Stories'].value = value

    @property
    def total_planned_tasks(self) -> PtcField:
        return self._fields['Total Planned Tasks']

    @total_planned_tasks.setter
    def total_planned_tasks(self, value: str) -> None:
        self._fields['Total Planned Tasks'].value = value

    @property
    def released_in(self) -> PtcField:
        return self._fields['Released In']

    @released_in.setter
    def released_in(self, value: str) -> None:
        self._fields['Released In'].value = value

    @property
    def total_remaining_user_stories(self) -> PtcField:
        return self._fields['Total Remaining User Stories']

    @total_remaining_user_stories.setter
    def total_remaining_user_stories(self, value: str) -> None:
        self._fields['Total Remaining User Stories'].value = value

    @property
    def total_remaining_tasks(self) -> PtcField:
        return self._fields['Total Remaining Tasks']

    @total_remaining_tasks.setter
    def total_remaining_tasks(self, value: str) -> None:
        self._fields['Total Remaining Tasks'].value = value

class Epic(PtcItem):
    """Attributes and Methods of a PTC Windchill User Story Item"""
    def __init__(self, epic_id):
        super().__init__(epic_id)
        self.fields.update(
            {
                'Responsible Team': PtcField('Responsible Team'),
                'Related Agile Product': PtcField('Related Agile Product'),
                'Split Into': PtcField('Split Into'),
                'Total User Stories Planned in Epic': PtcField('Total User Stories Planned in Epic'),
                'Total User Stories Implemented in Epic': PtcField('Total User Stories Implemented in Epic'),
                'Total Story Points Planned in Epic': PtcField('Total Story Points Planned in Epic'),
                'Remaining Story Points in Epic': PtcField('Remaining Story Points in Epic'),
                'Included in Sprints': PtcField('Included in Sprints'),
                'Feature': PtcField('Feature'),
                'Cancelled Comment': PtcField('Cancelled Comment')
            }
        )
        self.update_fields()

    @property
    def split_into(self) -> PtcField:
        return self._fields['Split Into']

    @split_into.setter
    def split_into(self, value: str) -> None:
        self._fields['Split Into'].value = value

    @property
    def total_user_stories_planned_in_epic(self) -> PtcField:
        return self._fields['Split Into']

    @total_user_stories_planned_in_epic.setter
    def total_user_stories_planned_in_epic(self, value: str) -> None:
        self._fields['Total User Stories Planned in Epic'].value = value

    @property
    def total_user_stories_implemented_in_epic(self) -> PtcField:
        return self._fields['Total User Stories Implemented in Epic']

    @total_user_stories_implemented_in_epic.setter
    def total_user_stories_implemented_in_epic(self, value: str) -> None:
        self._fields['Total User Stories Implemented in Epic'].value = value

    @property
    def total_story_points_planned_in_epic(self) -> PtcField:
        return self._fields['Total Story Points Planned in Epic']

    @total_story_points_planned_in_epic.setter
    def total_story_points_planned_in_epic(self, value: str) -> None:
        self._fields['Total Story Points Planned in Epic'].value = value

    @property
    def remaining_story_points_in_epic(self) -> PtcField:
        return self._fields['Remaining Story Points in Epic']

    @remaining_story_points_in_epic.setter
    def remaining_story_points_in_epic(self, value: str) -> None:
        self._fields['Remaining Story Points in Epic'].value = value

    @property
    def included_in_sprints(self) -> PtcField:
        return self._fields['Included in Sprints']

    @included_in_sprints.setter
    def included_in_sprints(self, value: str) -> None:
        self._fields['Included in Sprints'].value = value

    @property
    def feature(self) -> PtcField:
        return self._fields['Feature']

    @feature.setter
    def feature(self, value: str) -> None:
        self._fields['Feature'].value = value

    @property
    def cancelled_comment(self) -> PtcField:
        return self._fields['Cancelled Comment']

    @cancelled_comment.setter
    def cancelled_comment(self, value: str) -> None:
        self._fields['Cancelled Comment'].value = value

    @property
    def responsible_team(self) -> PtcField:
        return self._fields['Responsible Team']

    @responsible_team.setter
    def responsible_team(self, value: str) -> None:
        self._fields['Responsible Team'].value = value

    @property
    def related_agile_product(self) -> PtcField:
        return self._fields['Related Agile Product']

    @related_agile_product.setter
    def related_agile_product(self, value: str) -> None:
        self._fields['Related Agile Product'].value = value

class UserStory(PtcItem):
    """Attributes and Methods of a PTC Windchill User Story Item"""
    def __init__(self, us_id):
        super().__init__(us_id)
        self.fields.update(
            {
            'Responsible Team': PtcField('Responsible Team'),
            'Related Agile Product': PtcField('Related Agile Product'),
            'Split Into': PtcField('Split Into'),
            'Total Related Tasks': PtcField('Total Related Tasks'),
            'User Story included in Sprint': PtcField('User Story included in Sprint'),
            'Belongs To': PtcField('Belongs To'),
            'Component': PtcField('Component'),
            'Function': PtcField('Function'),
            'Variant': PtcField('Variant'),
            'Implementation Type': PtcField('Implementation Type'),
            'Product Cybersecurity Relevance': PtcField('Product Cybersecurity Relevance'),
            'Functional Safety Classification': PtcField('Functional Safety Classification'),
            'User Story Released In': PtcField('User Story Released In'),
            'Cancelled Comment': PtcField('Cancelled Comment'),
            }
        )
        self.update_fields()
        self.task_list = list()
        self.get_list_of_tasks()

    @property
    def responsible_team(self) -> PtcField:
        return self._fields['Responsible Team']

    @responsible_team.setter
    def responsible_team(self, value: str) -> None:
        self._fields['Responsible Team'].value = value

    @property
    def related_agile_product(self) -> PtcField:
        return self._fields['Related Agile Product']

    @related_agile_product.setter
    def related_agile_product(self, value: str) -> None:
        self._fields['Related Agile Product'].value = value

    @property
    def split_into(self) -> PtcField:
        return self._fields['Split Into']

    @split_into.setter
    def split_into(self, value: str) -> None:
        self._fields['Split Into'].value = value

    @property
    def total_related_tasks(self) -> PtcField:
        return self._fields['Total Related Tasks']

    @total_related_tasks.setter
    def total_related_tasks(self, value: str) -> None:
        self._fields['Total Related Tasks'].value = value

    @property
    def user_story_included_in_sprint(self) -> PtcField:
        return self._fields['User Story included in Sprint']

    @user_story_included_in_sprint.setter
    def user_story_included_in_sprint(self, value: str) -> None:
        self._fields['User Story included in Sprint'].value = value

    @property
    def belongs_to(self) -> PtcField:
        return self._fields['Belongs To']

    @belongs_to.setter
    def belongs_to(self, value: str) -> None:
        self._fields['Belongs To'].value = value

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
    def variant(self) -> PtcField:
        return self._fields['Variant']

    @variant.setter
    def variant(self, value: str) -> None:
        self._fields['Variant'].value = value

    @property
    def implementation_type(self) -> PtcField:
        return self._fields['Implementation Type']

    @implementation_type.setter
    def implementation_type(self, value: str) -> None:
        self._fields['Implementation Type'].value = value

    @property
    def product_cybersecurity_relevance(self) -> PtcField:
        return self._fields['Product Cybersecurity Relevance']

    @product_cybersecurity_relevance.setter
    def product_cybersecurity_relevance(self, value: str) -> None:
        self._fields['Product Cybersecurity Relevance'].value = value

    @property
    def functional_safety_classification(self) -> PtcField:
        return self._fields['Functional Safety Classification']

    @functional_safety_classification.setter
    def functional_safety_classification(self, value: str) -> None:
        self._fields['Functional Safety Classification'].value = value

    @property
    def user_story_released_in(self) -> PtcField:
        return self._fields['User Story Released In']

    @user_story_released_in.setter
    def user_story_released_in(self, value: str) -> None:
        self._fields['User Story Released In'].value = value

    @property
    def cancelled_comment(self) -> PtcField:
        return self._fields['Cancelled Comment']

    @cancelled_comment.setter
    def cancelled_comment(self, value: str) -> None:
        self._fields['Cancelled Comment'].value = value

    def get_list_of_tasks(self):
        spinto = self.split_into.value.replace(' ', '').split(',')
        for t in spinto:
            self.task_list.append(Task(t))

class Task(PtcItem):
    """Attributes and Methods of a PTC Windchill Task Item"""
    def __init__(self, task_id):
        super().__init__(task_id)
        self.fields.update(
            {
                'Responsible Team': PtcField('Responsible Team'),
                'Total Actual Effort': PtcField('Total Actual Effort'),
                'Total Estimated Effort': PtcField('Total Estimated Effort'),
                'Date Completed': PtcField('Date Completed'),
                'Task included in Sprint': PtcField('Task included in Sprint'),
                'Belongs To': PtcField('Belongs To'),
                'Is Input For': PtcField('Is Input For'),
                'Is Input From': PtcField('Is Input From'),
                'Cancelled Comment': PtcField('Cancelled Comment')
            }
        )
        self.update_fields()

    def __repr__(self) -> str:
        return super().__repr__()

    @property
    def responsible_team(self) -> PtcField:
        return self._fields['Responsible Team']

    @responsible_team.setter
    def responsible_team(self, value: str) -> None:
        self._fields['Responsible Team'].value = value

    @property
    def total_actual_effort(self) -> PtcField:
        return self._fields['Total Actual Effort']

    @total_actual_effort.setter
    def total_actual_effort(self, value: str) -> None:
        self._fields['Total Actual Effort'].value = value

    @property
    def total_estimated_effort(self) -> PtcField:
        return self._fields['Total Estimated Effort']

    @total_estimated_effort.setter
    def total_estimated_effort(self, value: str) -> None:
        self._fields['Total Estimated Effort'].value = value

    @property
    def date_completed(self) -> PtcField:
        return self._fields['Date Completed']

    @date_completed.setter
    def date_completed(self, value: str) -> None:
        self._fields['Date Completed'].value = value

    @property
    def task_included_in_sprint(self) -> PtcField:
        return self._fields['Task included in Sprint']

    @task_included_in_sprint.setter
    def task_included_in_sprint(self, value: str) -> None:
        self._fields['Task included in Sprint'].value = value

    @property
    def belongs_to(self) -> PtcField:
        return self._fields['Belongs To']

    @belongs_to.setter
    def belongs_to(self, value: str) -> None:
        self._fields['Belongs To'].value = value

    @property
    def is_input_for(self) -> PtcField:
        return self._fields['Is Input For']

    @is_input_for.setter
    def is_input_for(self, value: str) -> None:
        self._fields['Is Input For'].value = value

    @property
    def is_input_from(self) -> PtcField:
        return self._fields['Is Input From']

    @is_input_from.setter
    def is_input_from(self, value: str) -> None:
        self._fields['Is Input From'].value = value

    @property
    def cancelled_comment(self) -> PtcField:
        return self._fields['Cancelled Comment']

    @cancelled_comment.setter
    def cancelled_comment(self, value: str) -> None:
        self._fields['Cancelled Comment'].value = value

    def cancel_task(self, cancel_comment):
        """
        cancel_comment: Comment needed in order to cancel the task
        """
        self.im_editissue(self.cancelled_comment.name, cancel_comment)
        self.im_editissue(self.state.name, 'Cancelled')
        self.update_fields()
        if self.state.value == 'Cancelled':
            print(f'Task {self.id.value} cancelled')

class AgileProduct(PtcItem):
    """Attributes and Methods of a PTC Windchill Agile Product Item"""

    def __init__(self, ap_id):
        super().__init__(ap_id)
        self.fields.update(
            {
                'Part Of': PtcField('Part Of'),
                'Product Owner': PtcField('Product Owner'),
                'Epic': PtcField('Epic'),
                'Completed Epics': PtcField('Completed Epics'),
                'Cancelled Epics': PtcField('Cancelled Epics'),
                'Blocked Epics': PtcField('Blocked Epics'),
                'Completed Epics Count': PtcField('Completed Epics Count'),
                'Open Epics Count': PtcField('Open Epics Count'),
                'Cancelled Epics Count': PtcField('Cancelled Epics Count'),
                'Blocked Epics Count': PtcField('Blocked Epics Count'),
                'Total Epics Count': PtcField('Total Epics Count'),
                'User Story': PtcField('User Story'),
            }
        )
        self.update_fields()

    @property
    def part_of(self) -> PtcField:
        return self._fields['Part Of']

    @part_of.setter
    def part_of(self, value: str) -> None:
        self._fields['Part Of'].value = value

    @property
    def product_owner(self) -> PtcField:
        return self._fields['Product Owner']

    @product_owner.setter
    def product_owner(self, value: str) -> None:
        self._fields['Product Owner'].value = value

    @property
    def epic(self) -> PtcField:
        return self._fields['Epic']

    @epic.setter
    def epic(self, value: str) -> None:
        self._fields['Epic'].value = value

    @property
    def completed_epics(self) -> PtcField:
        return self._fields['Completed Epics']

    @completed_epics.setter
    def completed_epics(self, value: str) -> None:
        self._fields['Completed Epics'].value = value

    @property
    def cancelled_epics(self) -> PtcField:
        return self._fields['Cancelled Epics']

    @cancelled_epics.setter
    def cancelled_epics(self, value: str) -> None:
        self._fields['Cancelled Epics'].value = value

    @property
    def blocked_epics(self) -> PtcField:
        return self._fields['Blocked Epics']

    @blocked_epics.setter
    def blocked_epics(self, value: str) -> None:
        self._fields['Blocked Epics'].value = value

    @property
    def completed_epics_count(self) -> PtcField:
        return self._fields['Completed Epics Count']

    @completed_epics_count.setter
    def completed_epics_count(self, value: str) -> None:
        self._fields['Completed Epics Count'].value = value

    @property
    def open_epics_count(self) -> PtcField:
        return self._fields['Open Epics Count']

    @open_epics_count.setter
    def open_epics_count(self, value: str) -> None:
        self._fields['Open Epics Count'].value = value

    @property
    def cancelled_epics_count(self) -> PtcField:
        return self._fields['Cancelled Epics Count']

    @cancelled_epics_count.setter
    def cancelled_epics_count(self, value: str) -> None:
        self._fields['Cancelled Epics Count'].value = value

    @property
    def blocked_epics_count(self) -> PtcField:
        return self._fields['Blocked Epics Count']

    @blocked_epics_count.setter
    def blocked_epics_count(self, value: str) -> None:
        self._fields['Blocked Epics Count'].value = value

    @property
    def total_epics_count(self) -> PtcField:
        return self._fields['Total Epics Count']

    @total_epics_count.setter
    def total_epics_count(self, value: str) -> None:
        self._fields['Total Epics Count'].value = value

    @property
    def user_story(self) -> PtcField:
        return self._fields['User Story']

    @user_story.setter
    def user_story(self, value: str) -> None:
        self._fields['User Story'].value = value
#
#         self.completed_user_stories = PtcField('Completed User Stories')
#         self.fields.append(self.completed_user_stories)
#
#         self.cancelled_user_stories = PtcField('Cancelled User Stories')
#         self.fields.append(self.cancelled_user_stories)
#
#         self.blocked_user_stories = PtcField('Blocked User Stories')
#         self.fields.append(self.blocked_user_stories)
#
#         self.completed_user_stories_count = PtcField('Completed User Stories Count')
#         self.fields.append(self.completed_user_stories_count)
#
#         self.completed_user_stories_count = PtcField('Completed User Stories Count')
#         self.fields.append(self.completed_user_stories_count)
#
#         self.blocked_user_stories_count = PtcField('Blocked User Stories Count')
#         self.fields.append(self.blocked_user_stories_count)
#
#         self.total_user_stories_count = PtcField('Total User Stories Count')
#         self.fields.append(self.total_user_stories_count)
#
#         self.open_tasks_count = PtcField('Open tasks Count')
#         self.fields.append(self.open_tasks_count)
#
#         self.completed_tasks_count = PtcField('Completed tasks Count')
#         self.fields.append(self.completed_tasks_count)
#
#         self.cancelled_tasks_count = PtcField('Cancelled tasks Count')
#         self.fields.append(self.cancelled_tasks_count)
#
#         self.total_tasks_count = PtcField('Total tasks Count')
#         self.fields.append(self.total_tasks_count)
#
#         self.active_sprints = PtcField('Active Sprints')
#         self.fields.append(self.active_sprints)
#
#         self.completed_sprints = PtcField('Completed Sprints')
#         self.fields.append(self.completed_sprints)
#
#         self.cancelled_sprints = PtcField('Cancelled Sprints')
#         self.fields.append(self.cancelled_sprints)
#
#         self.total_sprints_count = PtcField('Total Sprints Count')
#         self.fields.append(self.total_sprints_count)
#
#         self.open_sprints_count = PtcField('Open Sprints Count')
#         self.fields.append(self.open_sprints_count)
#
#         self.completed_sprints_count = PtcField('Completed Sprints Count')
#         self.fields.append(self.completed_sprints_count)
#
#         self.cancelled_sprints_count = PtcField('Cancelled Sprints Count')
#         self.fields.append(self.cancelled_sprints_count)
