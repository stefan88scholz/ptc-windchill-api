from PtcItems import Sprint, UserStory, ItemIdNotNumeric

SPRINT_NR_CURRENT = '20418496'
SPRINT_NR_NEW = '20446116'

def update_sprint():
    sprint_old = Sprint(SPRINT_NR_CURRENT)
    sprint_new = Sprint(SPRINT_NR_NEW)
    #Get list of user stories
    user_stories = sprint_old.user_stories_in_sprint.value
    user_stories = user_stories.replace(' ','').split(',')
    if user_stories[0] != '':
        for us in user_stories:
            try:
                us_item = UserStory(us)
            except ItemIdNotNumeric as e:
                print(f'Exception occured {e}')
            else:
                if us_item.state.value == 'Defined' or us_item.state.value == 'In Progress':
                    # First remove current Sprint assignment
                    us_item.removefieldvalue(us_item.user_story_included_in_sprint.name, us_item.user_story_included_in_sprint.value)
                    # Now add new Sprint assignment
                    us_item.addfieldvalue(us_item.user_story_included_in_sprint.name, sprint_new.id.value)

            # Set old Sprint to Completed
            state = 'Unspecified'
            if sprint_old.state.value == 'Planned' or sprint_old.state.value == 'In Progress':
                while sprint_old.state.value != 'Completed':
                    if sprint_old.state.value == 'Planned':
                        sprint_old.im_editissue(sprint_old.state.name, 'In Progress')
                    elif sprint_old.state.value == 'In Progress':
                        sprint_old.im_editissue(sprint_old.state.name, 'Completed')
                    sprint_old.update_fields()
            print(f'Sprint {sprint_old.item_id} in state Completed')

        # Set new Sprint to In Progress
        if sprint_new.state.value == 'Planned':
            sprint_new.im_editissue(sprint_new.state.name, 'In Progress')
            print(f'Sprint {sprint_new.item_id} in state Completed')
        else:
            print(f'Sprint {sprint_new.item_id} not in state Planned')

update_sprint()

