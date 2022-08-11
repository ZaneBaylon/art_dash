import yaml
# import scratch

# def get_key(choice, sub_list):
# 	temp = []
# 	for i in choice:
# 		for key, value in sub_list.items():
# 			if i == value:
# 				temp.append(key)
# 	return temp

# sub_list = {"one":1, "two":2, "three":3}
# choice = [1,3]
# item = (get_key(choice, sub_list))
# print(item[1])

# ## try to put on yaml

# strValue = "Look him pp [M] (winterblueart)"
# ch1 = '['
# ch2 = ']'
# # Remove all characters before the character '-' from string
# listOfWords = strValue.split(ch1, 1)
# strValue = listOfWords[1]
# listOfWords = strValue.split(ch2, 1)
# strValue = listOfWords[0]
# print(strValue)

# print(scratch.x)

# choice = [2]
# sub_list = {"r/BreadTapedToTrees": 1, "r/Footpaws": 2, "r/furry_catwalk": 3}

with open("config.yaml", 'r') as stream:
    try:
        parameters = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        raise exc

sub_list = parameters.get('sub_list')
choice = parameters.get('choice', [])

def get_key(choice, sub_list):
    temp = []
    for i in choice:
        for key, value in sub_list.items():
            if i == value:
                temp.append(key)
    return temp


sub_choice = get_key(choice, sub_list)
print(sub_choice)