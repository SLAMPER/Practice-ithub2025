import json
import re
from tinydb import TinyDB

template_db = TinyDB('templates_data.json', encoding='utf-8')
template_collection = template_db.table('_default')

test_samples = [
    {"login": "petr@mail.com", "tel": "+7 999 888 77 66"},  
    {"customer": "Ольга", "дата_заказа": "2024-12-31"},  
    {"user_phone": "+7 800 555 35 35"},  
    {"user_email": "info@company.com", "user_phone": "+7 495 123 45 67"},  
    {"login": "alexey@gmail.com", "tel": "+7 916 999 00 11"},  
    {"customer": "Сергей", "order_id": "A-100", "дата_заказа": "2024-06-15"},  
]

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

def find_best_template(input_fields):
    field_categories = {k: determine_value_type(v) for k, v in input_fields.items()}
    selected_template = None
    max_matches = 0
    
    for record in template_collection.all():
        record_fields = {k: v for k, v in record.items() if k != 'name'}
        match_count = sum(
            1 for field, data_type in record_fields.items()
            if field in field_categories and field_categories[field] == data_type
        )
        
        if match_count > max_matches:
            max_matches = match_count
            selected_template = record['name']
    
    return {"matched_template": selected_template} if selected_template else {"detected_types": field_categories}

def run_test_cases():
    for sample in test_samples:
        print("Тестовые данные:", json.dumps(sample, ensure_ascii=False))
        output = find_best_template(sample)
        print("Результат:", json.dumps(output, indent=2, ensure_ascii=False))
        print("-" * 50)

if __name__ == "__main__":
    run_test_cases()