import json

"""Creates a JSON file for storing suffixes for different object types"""
suffixes = {'mesh': '_geo',
            'joint': '_jnt',
            'nurbsCurve': '_crv',
            'locator': '_loc',
            'light': "_lgt",
            'group': "_grp"}
try:
    with open('Database/SuffixDatabase.json', 'w') as data_file:
        json.dump(suffixes, data_file, indent=2)
except ValueError as write_error:
    print("Database could not be created.", write_error)
