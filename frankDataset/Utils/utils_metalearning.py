import sys
from Dataset.Wisdm import actNameWisdm
from Dataset.Wharf import actNameWharf
from Dataset.Mhealth import actNameMhealth
from Dataset.Pamap2 import actNamePamap2
from Dataset.Uschad import actNameUschad

actNameWisdm = actNameWisdm.values()
actNameWharf = actNameWharf.values()
actNameMhealth = actNameMhealth.values()
actNamePamap2 = actNamePamap2.values()
actNameUschad = actNameUschad.values()


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


def different_from_top4(dataset_name):
    """
    Return a list of all activities except the top4
    from a given dataset using
    the format "dataset-activity"
    """

    output = []
    dataset_act = globals()['actName' + dataset_name.upper()]
    top_4 = target_task_top4(dataset_name)
    for act in dataset_act:
        act_name = dataset_name + '-' + act.lower()
        if act_name not in top_4:
            output.append(act_name)
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