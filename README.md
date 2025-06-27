# Practice-ithub2025
# Практика

Задание подразумевает создание приложения, позволяющая находить формы по заданным значениям и типам данных.


# Установка и использование

1. Для использования этого приложения потребуется установить tinydb 
    ```python 
    pip install tinydb
2. Откройте cmd внутри репозитория. Для ручного ручного поиска формы вводите следующие команды используя данный формат:
     ```cmd
     python find_tpl.py get_tpl --field1=value1 --field2=value2
    ```
    Примеры:
    ```cmd
    python find_tpl.py get_tpl --login=user@example.com --tel="+7 123 456 78 90"
    python find_tpl.py get_tpl --customer="Иван Иванов" --дата_заказа="2024-12-31"
    ```
Для автоматизированного тестирования используйте следующую команду
```cmd
 > python tpl_matcher.py 
 ```

 Шаблоны представлены в виде json-файла и выглядит он следующим образом:

 ```javascript
 {
    "_default": {
        "1": {
            "name": "User profile",
            "login": "email",
            "tel": "phone"
        },
        "2": {
            "name": "Delivery form",
            "customer": "text",
            "order_id": "text",
            "дата_заказа": "date",
            "contact": "phone"
        },
        "3": {
            "name": "Support request",
            "user_email": "email",
            "user_phone": "phone",
            "issue_date": "date"
        }
    }
}
 ```
 Вы можете добавить свой шаблон используя пример сверху.


   
