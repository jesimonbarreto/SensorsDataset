import sys

actNameMHEALTH = [
    'Standing',
    'Sitting',
    'Lying down',
    'Walking',
    'Climbing stairs',
    'Waist bends forward',
    'Frontal elevation of lower_arms',
    'Knees bending (crouching)',
    'Cycling',
    'Jogging',
    'Running',
    'Jump front & back'
]

actNamePAMAP2 = [
    'Lying',
    'Sitting',
    'Standing',
    'Walking',
    'Running',
    'cycling',
    'Nordic walking',
    'watching TV',
    'computer work',
    'car driving',
    'ascending stairs',
    'descending stairs',
    'vacuum cleaning',
    'ironing',
    'folding laundry',
    'house cleaning',
    'playing soccer',
    'rope jumping'
]

actNameUSCHAD = [
    'Walking Forward',
    'Walking Left',
    'Walking Right',
    'Walking Upstairs',
    'Walking Downstairs',
    'Running Forward',
    'Jumping Up',
    'Sitting',
    'Standing',
    'Sleeping',
    'Elevator Up',
    'Elevator Down',
]

actNameWHARF = [
    'Brush teeth',
    'Climb stairs',
    'Comb hair',
    'Descend stairs',
    'Drinking glass',
    'Eat meat',
    'Ead soup',
    'Get up bed',
    'Lie down bed',
    'Pour water',
    'Sit down chair',
    'Stand up chair',
    'Walk',
    'Use telephone'
]


actNameWISDM = [
    'Walking',
    'Jogging',
    'Upstairs',
    'Downstairs',
    'Sitting',
    'Standing'
]


def all_activities(dataset_name):
    """
    Return a list of all activities
    from a given dataset using
    the format "dataset-activity"
    """

    output = []
    dataset_act = globals()['actName' + dataset_name.upper()]
    for act in dataset_act:
        output.append(dataset_name + '-' + act.lower())
    return output


def target_task_top4(dataset_name):
    """
       Return a list with the names of the top4 most common activities
       walking, upstairs, sitting, standing
       from a given dataset using the format "dataset-activity"

    """
    output = []
    if dataset_name.upper() == 'MHEALTH':
        acts = ['Walking', 'Climbing stairs', 'Sitting', 'Standing']
        for act in acts:
            output.append(dataset_name + '-' + act.lower())
    elif dataset_name.upper() == 'PAMAP2':
        acts =['Walking', 'ascending stairs', 'Sitting', 'Standing']
        for act in acts:
            output.append(dataset_name + '-' + act.lower())
    elif dataset_name.upper() == 'USCHAD':
        acts = ['Walking Forward', 'Walking Upstairs', 'Sitting', 'Standing']
        for act in acts:
            output.append(dataset_name + '-' + act.lower())
    elif dataset_name.upper() == 'WHARF':
        acts = ['Walk', 'Climb stairs', 'Sit down chair', 'Stand up chair']
        for act in acts:
            output.append(dataset_name + '-' + act.lower())
    elif dataset_name.upper() == 'WISDM':
        acts = ['Walking', 'Upstairs', 'Sitting', 'Standing']
        for act in acts:
            output.append(dataset_name + '-' + act.lower())
    else:
        sys.exit("O dataset {} não é aceito".format(dataset_name))

    return output


if __name__ == '__main__':
    print(all_activities('uschad'))