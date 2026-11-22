import datetime
from collections import UserDict
from dataclasses import dataclass, field

from get_upcoming_birthday import get_upcoming_birthdays


@dataclass  
class Field:   # Base class for all field types
    value: str

    def __str__(self):
        return str(self.value)


@dataclass
class Name(Field): # Name field class
    def __post_init__(self):
        if not self.value or not str(self.value).strip():
            raise ValueError("Name is required.")


@dataclass
class Phone(Field): # Phone field class
    def __post_init__(self):
        self.value = str(self.value)
        if not (self.value.isdigit() and len(self.value) == 10): #  Check if the phone number contains exactly 10 digits
            raise ValueError("Phone number must contain exactly 10 digits.")


@dataclass
class Birthday(Field): # Birthday field class
    def __post_init__(self):
        try:
            # Validate the DD.MM.YYYY format and convert the string to a datetime object
            self.value = datetime.datetime.strptime(str(self.value), "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


@dataclass
class Record: # Record class to hold a contact's name, phone numbers and birthday
    name: Name
    phones: list[Phone] = field(default_factory=list)
    birthday: Birthday | None = None

    def __post_init__(self):
        if not isinstance(self.name, Name):
            self.name = Name(self.name)

    def add_phone(self, phone): # Add a phone number to the record
        self.phones.append(Phone(phone))

    def find_phone(self, phone): # Find a phone number in the record
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone): # Remove a phone number from the record
        found = self.find_phone(phone)
        if found is None:
            raise ValueError(f"Phone {phone} not found.")
        self.phones.remove(found)

    def edit_phone(self, old_phone, new_phone): # Edit a phone number in the record
        found = self.find_phone(old_phone)
        if found is None:
            raise ValueError(f"Phone {old_phone} not found.") # Print an error message if the old phone number is not found
        new = Phone(new_phone)
        self.phones[self.phones.index(found)] = new

    def add_birthday(self, birthday): # Add a birthday to the record (only one is allowed)
        if self.birthday is not None:
            raise ValueError("Birthday already exists for this contact.")
        self.birthday = Birthday(birthday)

    def __str__(self):
        result = f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        if self.birthday:
            result += f", birthday: {self.birthday}"
        return result


class AddressBook(UserDict): # AddressBook class to hold multiple records
    
    def add_record(self, record):  # Add a record to the address book
        self.data[record.name.value] = record

    def find(self, name):  # Find a record by name in the address book
        return self.data.get(name)

    def delete(self, name): # Delete a record by name from the address book
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self): # Return contacts to congratulate during the next 7 days
        users = [
            (record.name.value, record.birthday.value.date())
            for record in self.data.values()
            if record.birthday is not None
        ]
        return [
            {'name': name, 'congratulation_date': date.strftime('%d.%m.%Y')}
            for name, date in get_upcoming_birthdays(users)
        ]


if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john) 

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  

    john.add_birthday("20.11.1990")
    print(john)
    print(book.get_upcoming_birthdays())

    book.delete("Jane")
