import yaml
import pyperclip


# data = str(pyperclip.paste())
# dataY = dict(Data = data)

# with open('test.yaml', 'a') as outfile:
#     yaml.dump(dataY, outfile, default_flow_style=False)

# num = ["3"]
# numY = dict(Num = num)

# with open('test.yaml', 'a') as outfile:
#     yaml.dump(numY, outfile, default_flow_style=False)

# with open("test.yaml", 'r') as stream:
#     try:
#         parameters = yaml.safe_load(stream)
#     except yaml.YAMLError as exc:
#         raise exc

#     data = parameters.get('Data')
#     print(data)

#     hello = "poop"
#     print(hello)

key = ["one", "two"]

string = "contains(., '" +key[0]+ "') or contains(., '" +key[1]+ "')"

print(string)