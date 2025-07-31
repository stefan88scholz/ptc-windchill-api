import subprocess
from abc import ABC, abstractmethod
from PtcDefines import *

class ItemIdNotNumeric(Exception):
    """ Exception raised if Item Id not numeric"""
    def __init__(self, message: str, error_code: str = '') -> None:
        super().__init__(message)
        self.message: str    = message
        self.error_code: str = error_code

    def __str__(self) -> str:
        return f'{self.message} (Error Code: {self.error_code})'

class PtcField:
    def __init__(self, name: str, value: str = 'None') -> None:
        self.name: str  = name
        self.value: str = value

    def __repr__(self) -> str:
        return f'{self.name}: {self.value}'


class PtcItem():
    """ Attributes and Methods of PTC Windchill items"""
    def __init__(self, item_id: int):
        if not isinstance(item_id,int) and (isinstance(item_id, str) and not item_id.isnumeric()):
            raise ItemIdNotNumeric(f'Item with ID {item_id} is not numeric')
        self.item_id: int                   = int(item_id)
        self.fields: list[PtcField] = list()
        self.id: PtcField = PtcField('ID', item_id)
        self.fields.append(self.id)

        self.type: PtcField = PtcField('Type')
        self.fields.append(self.type)

        self.summary: PtcField = PtcField('Summary')
        self.fields.append(self.summary)

        self.state: PtcField = PtcField('State')
        self.fields.append(self.state)

        self.project: PtcField = PtcField('Project')
        self.fields.append(self.project)

        self.assigned_user: PtcField = PtcField('Assigned User')
        self.fields.append(self.assigned_user)

        self.item_report_raw: str  = ''

    def __str__(self) -> str:
        result: str = str()
        for field in self.fields:
            result = result + field.name + ': ' + field.value + '\n'
        return result

    def update_fields(self) -> None:
        for field in self.itemreport():
            for i in range(0, len(self.fields)):
                if field.startswith(self.fields[i].name + ':'):
                    self.fields[i].value = field.replace(self.fields[i].name + ': ', '')

    def removefieldvalue(self, field_name: str, field_value: str):
        #print(f'im editissue --removeFieldValues=\'{field_name}={field_value}\' {self.item_id}')
        subprocess.run(f'im editissue --removeFieldValues=\'{field_name}={field_value}\' {self.item_id}',
                       stdout=subprocess.PIPE)

    def addfieldvalue(self, field_name: str, field_value: str):
        #print(f'im editissue --addFieldValues=\'{field_name}={field_value}\' {self.item_id}')
        subprocess.run(f'im editissue --addFieldValues=\'{field_name}={field_value}\' {self.item_id}',
                       stdout=subprocess.PIPE)

    def itemreport(self):
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
        return subprocess.run(f'im editissue --field=\'{field_name}={field_value}\' {self.item_id}')

    def im_viewissue(self):
        #print(f'im viewissue {self.item_id}')
        return subprocess.run(f'im viewissue {self.item_id}', stdout=subprocess.PIPE)

class WorkItem(PtcItem):
    def __init__(self, work_item_id: int | str) -> None:
        super().__init__(work_item_id)
        self.component: PtcField = PtcField('Component')
        self.fields.append(self.component)

        self.variant: PtcField   = PtcField('Variant')
        self.fields.append(self.variant)

        self.contains_items: PtcField   = PtcField('Contains Items')
        self.fields.append(self.contains_items)

        self.belongs_to_work_item: PtcField   = PtcField('Belongs To Work Item')
        self.fields.append(self.belongs_to_work_item)

        self.update_fields()

class Sprint(PtcItem):
    """Attributes and Methods of a PTC Windchill Sprint Item"""
    def __init__(self, sprint_id):
        super().__init__(sprint_id)
        self.responsible_team: PtcField             = PtcField('Responsible Team')
        self.fields.append(self.responsible_team)

        self.related_agile_product: PtcField        = PtcField('Related Agile Product')
        self.fields.append(self.related_agile_product)

        self.user_stories_in_sprint: PtcField       = PtcField('User Stories in Sprint')
        self.fields.append(self.user_stories_in_sprint)

        self.sprint_tested_by: PtcField             = PtcField('Sprint Tested By')
        self.fields.append(self.sprint_tested_by)

        self.tasks_in_sprint: PtcField              = PtcField('Tasks in Sprint')
        self.fields.append(self.tasks_in_sprint)

        self.total_planned_user_stories: PtcField   = PtcField('Total Planned User Stories')
        self.fields.append(self.total_planned_user_stories)

        self.total_planned_tasks: PtcField          = PtcField('Total Planned Tasks')
        self.fields.append(self.total_planned_tasks)

        self.released_in: PtcField                  = PtcField('Released In')
        self.fields.append(self.released_in)

        self.total_remaining_user_stories: PtcField = PtcField('Total Remaining User Stories')
        self.fields.append(self.total_remaining_user_stories)

        self.total_remaining_tasks: PtcField  = PtcField('Total Remaining Tasks')
        self.fields.append(self.total_remaining_tasks)

        self.update_fields()

class Epic(PtcItem):
    """Attributes and Methods of a PTC Windchill User Story Item"""
    def __init__(self, epic_id):
        super().__init__(epic_id)
        self.responsible_team: PtcField = PtcField('Responsible Team')
        self.fields.append(self.responsible_team)

        self.related_agile_product: PtcField = PtcField('Related Agile Product')
        self.fields.append(self.related_agile_product)

        self.split_into: PtcField = PtcField('Split Into')
        self.fields.append(self.split_into)

        self.total_user_stories_planned_in_epic: PtcField = PtcField('Total User Stories Planned in Epic')
        self.fields.append(self.total_user_stories_planned_in_epic)

        self.total_user_stories_implemented_in_epic: PtcField = PtcField('Total User Stories Implemented in Epic')
        self.fields.append(self.total_user_stories_implemented_in_epic)

        self.total_story_points_planned_in_epic: PtcField = PtcField('Total Story Points Planned in Epic')
        self.fields.append(self.total_story_points_planned_in_epic)

        self.remaining_story_points_in_epic: PtcField = PtcField('Remaining Story Points in Epic')
        self.fields.append(self.remaining_story_points_in_epic)

        self.included_in_sprints: PtcField = PtcField('Included in Sprints')
        self.fields.append(self.included_in_sprints)

        self.feature: PtcField = PtcField('Feature')
        self.fields.append(self.feature)

        self.cancelled_comment: PtcField = PtcField('Cancelled Comment')
        self.fields.append(self.cancelled_comment)
        self.update_fields()

class UserStory(PtcItem):
    """Attributes and Methods of a PTC Windchill User Story Item"""
    def __init__(self, us_id):
        super().__init__(us_id)

        self.responsible_team: PtcField = PtcField('Responsible Team')
        self.fields.append(self.responsible_team)

        self.related_agile_product: PtcField = PtcField('Related Agile Product')
        self.fields.append(self.related_agile_product)

        self.split_into: PtcField = PtcField('Split Into')
        self.fields.append(self.split_into)

        self.total_related_tasks: PtcField = PtcField('Total Related Tasks')
        self.fields.append(self.total_related_tasks)

        self.user_story_included_in_sprint: PtcField = PtcField('User Story included in Sprint')
        self.fields.append(self.user_story_included_in_sprint)

        self.belongs_to: PtcField = PtcField('Belongs To')
        self.fields.append(self.belongs_to)

        self.component: PtcField = PtcField('Component')
        self.fields.append(self.component)

        self.function: PtcField = PtcField('Function')
        self.fields.append(self.function)

        self.variant: PtcField = PtcField('Variant')
        self.fields.append(self.variant)

        self.implementation_type: PtcField = PtcField('Implementation Type')
        self.fields.append(self.implementation_type)

        self.product_cybersecurity_classification: PtcField = PtcField('Product Cybersecurity Relevance')
        self.fields.append(self.product_cybersecurity_classification)

        self.functional_safety_classification: PtcField = PtcField('Functional Safety Classification')
        self.fields.append(self.functional_safety_classification)

        self.user_story_released_in: PtcField = PtcField('User Story Released In')
        self.fields.append(self.user_story_released_in)

        self.cancelled_comment: PtcField = PtcField('Cancelled Comment')
        self.fields.append(self.cancelled_comment)

        self.update_fields()
        self.task_list = list()
        self.get_list_of_tasks()

    def get_list_of_tasks(self):
        spinto = self.split_into.value.replace(' ', '').split(',')
        for t in spinto:
            self.task_list.append(Task(t))

    def set_sprint_id(self, sprint_id: str):
        self.addfieldvalue(self.user_story_included_in_sprint.name, sprint_id)

    def set_release(self, release_id: str):
        self.addfieldvalue(self.user_story_released_in.name, release_id)

class Task(PtcItem):
    """Attributes and Methods of a PTC Windchill Task Item"""
    def __init__(self, task_id):
        super().__init__(task_id)

        self.responsible_team: PtcField = PtcField('Responsible Team')
        self.fields.append(self.responsible_team)

        self.total_actual_effort: PtcField = PtcField('Total Actual Effort')
        self.fields.append(self.total_actual_effort)

        self.total_estimated_effort: PtcField = PtcField('Total Estimated Effort')
        self.fields.append(self.total_estimated_effort)

        self.date_completed: PtcField = PtcField('Date Completed')
        self.fields.append(self.date_completed)

        self.task_included_in_sprint: PtcField = PtcField('Task included in Sprint')
        self.fields.append(self.task_included_in_sprint)

        self.belongs_to: PtcField = PtcField('Belongs To')
        self.fields.append(self.belongs_to)

        self.is_input_for: PtcField = PtcField('Is Input For')
        self.fields.append(self.is_input_for)

        self.is_input_from: PtcField = PtcField('Is Input From')
        self.fields.append(self.is_input_from)

        self.cancelled_comment: PtcField = PtcField('Cancelled Comment')
        self.fields.append(self.cancelled_comment)

        super().update_fields()

    def cancel_task(self, cancel_comment):
        """
        cancel_comment: Comment needed in order to cancel the task
        """
        self.im_editissue(self.cancelled_comment.name, cancel_comment)
        self.im_editissue(self.state.name, STATE_CANCELLED)
        self.update_fields()
        if self.state.value == 'Cancelled':
            print(f'Task {self.id.value} cancelled')

class AgileProduct(PtcItem):
    """Attributes and Methods of a PTC Windchill Agile Product Item"""

    def __init__(self, ap_id):
        super().__init__(ap_id)

        self.part_of = PtcField('Part Of')
        self.fields.append(self.part_of)

        self.product_owner = PtcField('Product Owner')
        self.fields.append(self.product_owner)

        self.epic = PtcField('Epic')
        self.fields.append(self.epic)

        self.completed_epics = PtcField('Completed Epics')
        self.fields.append(self.completed_epics)

        self.cancelled_epics = PtcField('Cancelled Epics')
        self.fields.append(self.cancelled_epics)

        self.blocked_epics = PtcField('Blocked Epics')
        self.fields.append(self.blocked_epics)

        self.completed_epics_count = PtcField('Completed Epics Count')
        self.fields.append(self.completed_epics_count)

        self.open_epics_count = PtcField('Open Epics Count')
        self.fields.append(self.open_epics_count)

        self.cancelled_epics_count = PtcField('Cancelled Epics Count')
        self.fields.append(self.cancelled_epics_count)

        self.blocked_epics_count = PtcField('Blocked Epics Count')
        self.fields.append(self.blocked_epics_count)

        self.total_epics_count = PtcField('Total Epics Count')
        self.fields.append(self.total_epics_count)

        self.user_story = PtcField('User Story')
        self.fields.append(self.user_story)

        self.completed_user_stories = PtcField('Completed User Stories')
        self.fields.append(self.completed_user_stories)

        self.cancelled_user_stories = PtcField('Cancelled User Stories')
        self.fields.append(self.cancelled_user_stories)

        self.blocked_user_stories = PtcField('Blocked User Stories')
        self.fields.append(self.blocked_user_stories)

        self.completed_user_stories_count = PtcField('Completed User Stories Count')
        self.fields.append(self.completed_user_stories_count)

        self.completed_user_stories_count = PtcField('Completed User Stories Count')
        self.fields.append(self.completed_user_stories_count)

        self.blocked_user_stories_count = PtcField('Blocked User Stories Count')
        self.fields.append(self.blocked_user_stories_count)

        self.total_user_stories_count = PtcField('Total User Stories Count')
        self.fields.append(self.total_user_stories_count)

        self.open_tasks_count = PtcField('Open tasks Count')
        self.fields.append(self.open_tasks_count)

        self.completed_tasks_count = PtcField('Completed tasks Count')
        self.fields.append(self.completed_tasks_count)

        self.cancelled_tasks_count = PtcField('Cancelled tasks Count')
        self.fields.append(self.cancelled_tasks_count)

        self.total_tasks_count = PtcField('Total tasks Count')
        self.fields.append(self.total_tasks_count)

        self.active_sprints = PtcField('Active Sprints')
        self.fields.append(self.active_sprints)

        self.completed_sprints = PtcField('Completed Sprints')
        self.fields.append(self.completed_sprints)

        self.cancelled_sprints = PtcField('Cancelled Sprints')
        self.fields.append(self.cancelled_sprints)

        self.total_sprints_count = PtcField('Total Sprints Count')
        self.fields.append(self.total_sprints_count)

        self.open_sprints_count = PtcField('Open Sprints Count')
        self.fields.append(self.open_sprints_count)

        self.completed_sprints_count = PtcField('Completed Sprints Count')
        self.fields.append(self.completed_sprints_count)

        self.cancelled_sprints_count = PtcField('Cancelled Sprints Count')
        self.fields.append(self.cancelled_sprints_count)

        super().update_fields()

def main() -> None:
    pass

if __name__ == '__main__':
    main()
