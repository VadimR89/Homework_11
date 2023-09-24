from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday:
    def __init__(self, date):
        self.date = date

    def validate(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def set_value(self, new_value):
        if self.validate(new_value):
            self._value = new_value
        else:
            raise ValueError("Invalid birthday format")


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number format")

    def validate_phone(self, value):
        if len(value) == 10 and value.isdigit():
            return True
        else:
            return False

    def set_value(self, new_value):
        if self.validate_phone(new_value):
            self.value = new_value
        else:
            raise ValueError("Invalid phone number format")


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def set_birthday(self, birthday):
        if birthday is None:
            self.birthday = None
        else:
            birthday_obj = Birthday(birthday)
            if birthday_obj.validate():
                self.birthday = birthday_obj
            else:
                raise ValueError("Invalid birthday format")

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            next_birthday = datetime(today.year, self.birthday.date.month, self.birthday.date.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.date.month, self.birthday.date.day)
            days_left = (next_birthday - today).days
            return days_left
        else:
            raise ValueError("Birthday is not set for this record.")

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                phone_obj.value = new_phone
                found = True
        if not found:
            raise ValueError(f"Phone number '{old_phone}' not found in the record")

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, page_size):
        records = list(self.data.values())
        total_records = len(records)
        current_page = 0

        while current_page * page_size < total_records:
            start_idx = current_page * page_size
            end_idx = min((current_page + 1) * page_size, total_records)
            yield records[start_idx:end_idx]
            current_page += 1
