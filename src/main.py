import psutil
import json
import subprocess
import time
from PtcItems import UserStory
from PtcDocument import PtcDocument
from PtcDefines import *


#ProcessRunning = lambda : 'IntegrityClient.exe' in (p.name() for p in psutil.process_iter())

def getProcessStatus(Pname: str) -> bool:
    for process in psutil.process_iter():
        if process.name() == Pname:
            if process.status() == "running":
                return True
    return False

def startIntegrity():
    if not getProcessStatus("IntegrityClient.exe"):
        toolFound = False
        #print('Integrity client not running')
        with open('ToolList.json') as json_file:
            toolList = json.load(json_file)
            for tool in toolList:
                if tool["Name"] == "IntegrityClient.exe":
                    subprocess.run(tool["Process"])
                    toolFound = True
                    break # Stop the search
        if toolFound:
            print("Start Integrity Client and wait until process is running")
            t_end = time.time() + 5
            while time.time() < t_end:
                if getProcessStatus("IntegrityClient.exe"):
                    print("Integrity Client is running")
                    break
                else:
                    print("Process not running")
        else:
            print("Integrity not found")
    else:
        print("IntegrityClient.exe running")

def cancel_tasks_todo(cancel_comment, us_id):
    pass
    #user_story = UserStory(19362150)
    #for task in user_story.task_list:
        #if re.search('ReqEng',task.summary.value) or re.search('SQT',task.summary.value):
        #    task.cancel_task(cancel_comment)

def cancel_us(us_id, sprint_id, release_id, cancel_comment):
    user_story = UserStory(us_id)
    if user_story.state.value == STATE_DRAFT:
        user_story.im_editissue(user_story.state.name, STATE_DEFINED)
        user_story.update_fields()
    if user_story.state.value == STATE_DEFINED:
        if not user_story.user_story_included_in_sprint.value:
            user_story.im_editissue(user_story.user_story_included_in_sprint.name,sprint_id)
        if not user_story.user_story_released_in.value:
            user_story.addfieldvalue(user_story.user_story_released_in.name, release_id)
        user_story.im_editissue(user_story.state.name,STATE_IN_PROGRESS)
        user_story.update_fields()

    error = ''
    if user_story.state.value == STATE_IN_PROGRESS:
        if user_story.user_story_included_in_sprint.value == sprint_id:
            for task in user_story.task_list:
                if task.state.value == 'ToDo':
                    task.cancel_task(cancel_comment)

            for task in user_story.task_list:
                if task.state.value != 'Cancelled':
                    error = f'Task {task.id.value} not in state Cancelled'
                    break
    else:
        error = f'User Story {us_id} not in state {STATE_IN_PROGRESS}'
    if not error:
        user_story.im_editissue(user_story.cancelled_comment.name,cancel_comment)
        user_story.im_editissue(user_story.state.name,STATE_CANCELLED)
        user_story.removefieldvalue(user_story.user_story_included_in_sprint.name, sprint_id)
        user_story.removefieldvalue(user_story.user_story_released_in.name, release_id)
    else:
        print(error)

def update_interface() -> None:
    doc = PtcDocument(3530632)
    print(doc.document_short_title.value)
    # client_server = list()
    # for element in doc.elements:
    #     if element.interface_type.value == 'ClientServer':
    #         client_server.append(element)
    # update_interface(doc.elements, changes_auth_by='19390968', decomposed_from='20125464')
    #print(doc.elements)
    #inter = Interface(20075656)
    #print(inter.contains.value)
    # update_interface(Interface(20840726),
    #                  Interface(20840728),
    #                  Interface(20840730),
    #                  Interface(20840732),
    #                  Interface(20844835),
    #                  Interface(20844837),
    #                  Interface(20844872),
    #                  Interface(20844875),
    #                  Interface(20844878),
    #                  )

def update_requirement():
    shutdown_srs = list([20676507, 20676503, 20676775, 20677013])
    #shutdown_srs = list([20676507])
    for requirement in shutdown_srs:
        item = Requirement(requirement.__str__())
        #item.im_editissue(item.changes_authorized_by.name, '19367484')
        #item.im_editissue(item.item_owner.name                          , ITEM_OWNER_SCHOLSTA)
        #item.im_editissue(item.variant.name                             , VARIANT_IRWS_GEN2_SR_F3)
        #item.im_editissue(item.function.name                            , FUNCTION_OPMODE_SHUTDOWN)
        #item.im_editissue(item.item_maturity_level.name                 , ITEM_MATURITY_LEVEL1)
        #item.im_editissue(item.requirement_category.name                , REQ_CAT_FUNCTIONAL)
        #item.im_editissue(item.functional_safety_classification.name    , FUSA_CLS_NOT_APPLICABLE)
        #item.im_editissue(item.product_cybersecurity_classification.name, PRODUCT_CYBER_RELEVANT)
        #item.im_editissue(item.regulatory_relevance.name                , REGULARY_RELEVANCE_NOT_RELEVANT)
        #item.im_editissue(item.vnv_category.name                        , VNV_CATEGORY_SW_QT_VERIFY)
        #item.im_editissue(item.requirement_belongs_to_delivery.name,SR_IRWS_GEN2_SW_R07_00_00_PRL3_PLUS)
        #item.im_editissue(item.details.name, '18423853')
        item.im_editissue(item.state.name, 'In Review')
        if item.item_id == '20676507':
            #item.im_editissue(item.feature.name, FEATURE_iRWS_SW_ASC)
            #item.addfieldvalue(item.decomposes_to.name, '18704058')
            pass
        elif item.item_id == '20677013':
            #item.im_editissue(item.feature.name, FEATURE_iRWS_SW_PMIC)
            pass
        elif item.item_id == '20676775':
            #item.im_editissue(item.feature.name, FEATURE_iRWS_SW_GDU)
            #item.addfieldvalue(item.decomposes_to.name, '19739658')
            pass
        elif item.item_id == '20676503':
            #item.im_editissue(item.feature.name, FEATURE_iRWS_SW_GDU)
            #item.addfieldvalue(item.decomposes_to.name, '18704060,18704062')
            pass
        else:
            pass

        #print(item.item_owner.value)

def main():
    pass

if __name__ == '__main__':
    main()