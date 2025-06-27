import sys
import json
import re
from tinydb import TinyDB, Query

template_db = TinyDB('templates_data.json', encoding='utf-8')
template_collection = template_db.table('_default')

def execute():
    if len(sys.argv) < 2 or sys.argv[1] != 'get_tpl':
        print("Использование: python find_tpl.py get_tpl --поле=значение --поле2=значение2")
        return

    input_parameters = {}
    for argument in sys.argv[2:]:
        if argument.startswith('--') and '=' in argument:
            param_name, param_value = argument[2:].split('=', 1)
            input_parameters[param_name] = param_value

    if not input_parameters:
        print("Ошибка: параметры поиска не указаны")
        return

    parameter_types = {k: determine_value_type(v) for k, v in input_parameters.items()}
    best_template = None
    highest_match_count = 0
    
    for template in template_collection.all():
        template_title = template['name']
        template_fields = {k: v for k, v in template.items() if k != 'name'}
        
        current_matches = sum(
            1 for field, expected_type in template_fields.items()
            if field in parameter_types and parameter_types[field] == expected_type
        )
        
        if current_matches == len(template_fields):
            print(json.dumps({"template_name": template_title}, indent=2, ensure_ascii=False))
            return
        
        if current_matches > highest_match_count:
            highest_match_count = current_matches
            best_template = template_title

    if best_template and highest_match_count > 0:
        print(json.dumps({"template_name": best_template}, indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"parameter_types": parameter_types}, indent=2, ensure_ascii=False))

def determine_value_type(value):
    if not isinstance(value, str):
        return 'text'
    
    if re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
        return 'email'
    
    if re.fullmatch(r'^\+7 \d{3} \d{3} \d{2} \d{2}$', value):
        return 'phone'
    
    if (re.fullmatch(r'^\d{2}\.\d{2}\.\d{4}$', value) or 
        re.fullmatch(r'^\d{4}-\d{2}-\d{2}$', value)):
        return 'date'
    
    return 'text'

if __name__ == "__main__":
    execute()