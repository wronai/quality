# main.py - Kod z problemami jakości (celowo)

def process_user_data_with_many_parameters_and_complex_logic(user_id, first_name, last_name, email_address, phone_number, street_address, city_name, postal_code, country_code, date_of_birth, preferences, settings, metadata):
    if user_id:
        if first_name:
            if last_name:
                if email_address:
                    if phone_number:
                        if street_address:
                            if city_name:
                                if postal_code:
                                    result = {}
                                    result['id'] = user_id
                                    result['first'] = first_name.strip().title()
                                    result['last'] = last_name.strip().title()
                                    result['email'] = email_address.lower().strip()
                                    result['phone'] = phone_number.strip()
                                    result['address'] = street_address.strip()
                                    result['city'] = city_name.strip()
                                    result['postal'] = postal_code.strip()
                                    result['country'] = country_code
                                    result['birth'] = date_of_birth
                                    result['prefs'] = preferences
                                    result['settings'] = settings
                                    result['meta'] = metadata
                                    result['status'] = 'active'
                                    result['created'] = 'now'
                                    result['updated'] = 'now'
                                    return result
    return None

def another_function_without_documentation():
    data = [1, 2, 3, 4, 5]
    return sum(data)

if __name__ == "__main__":
    result = process_user_data_with_many_parameters_and_complex_logic(
        "123", "John", "Doe", "john@example.com", "+1234567890",
        "123 Main St", "Anytown", "12345", "US", "1990-01-01",
        {"theme": "dark"}, {"notifications": True}, {"source": "web"}
    )
    print(f"Result: {result}")

    result2 = another_function_without_documentation()
    print(f"Sum: {result2}")
