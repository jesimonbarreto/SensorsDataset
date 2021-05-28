import sys
from Dataset.Wisdm import actNameWISDM
from Dataset.Wharf import actNameWHARF
from Dataset.Mhealth import actNameMHEALTH
from Dataset.Pamap2 import actNamePAMAP2
from Dataset.Uschad import actNameUSCHAD

actNameWISDM = actNameWISDM.values()
actNameWHARF = actNameWHARF.values()
actNameMHEALTH = actNameMHEALTH.values()
actNamePAMAP2 = actNamePAMAP2.values()
actNameUSCHAD = actNameUSCHAD.values()


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


def all_activities_all_datasets(dataset_list):
    """
    Return a list of all activities
    from a given dataset using
    the format "dataset-activity"
    """

    output = []
    for dataset_name in dataset_list:
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
        acts = ['Walk Forward', 'Walk Up', 'Sit', 'Stand']
        for act in acts:
            output.append(dataset_name + '-' + act.lower())
    elif dataset_name.upper() == 'WHARF':
        acts = ['Walk', 'Climb stairs', 'Sitdown chair', 'Standup chair']
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