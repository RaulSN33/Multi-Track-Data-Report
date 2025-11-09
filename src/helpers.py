from numpy import nan

subjects = [
    'Math',
    'English',
    'Science',
    'History'
]

tracks = ['Data', 'BM', 'Finance']

replace_values_mapping_dict = {
    'nans':{
        'columns':subjects,
        'values_to_replace':{
            'WAIVE':nan,
            'WAIVED':nan
        }
    },
    'passed': {
        'columns':'Passed (Y/N)',
        'values_to_replace':{
            'no':'N',
            'y':'Y'
        }
    }
}
terms_mapping_dict = {
    1:'Fall',
    2:'Spring'
}
