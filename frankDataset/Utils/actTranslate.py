
actNameVersions = {
	'walking': ['walking forward'],
	'ascending stairs': ['walking up'],
	'descending stairs': ['walking down'],
	'walking down':['descending stairs'],
	'walking up':['ascending stairs'],
	'walking forward':['walking'],
	'lying':['lying'],
	'lying on back':['lying'],
	'lying on right':['lying'],
	'laying':['lying'],
	'sleeping':['lying'],
	'lying': ['sleeping','laying','lying on right','lying on back']
}
actNameStandardization = {
	'walking forward': 'walking',
	'walking up':'ascending stairs',
	'walking down': 'descending stairs',
	'lying on back': 'lying',
	'lying on right': 'lying',
	'laying': 'lying',
	'sleeping': 'lying'
}
def genericActNames(act):
	act = act.lower()
	if 'walking forward' in act:
		return 'walking'
	if 'walking up' in act:
		return 'ascending stairs'
	if 'walking down' in act:
		return 'descending stairs'
	if 'lying' in act or 'sleeping' in act or 'laying' in act:
		return 'lying'
	return act
