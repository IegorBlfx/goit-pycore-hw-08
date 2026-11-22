from classes import AddressBook, Record


def input_error(func): # Decorator to handle input errors
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            if "unpack" in str(e):
                return "Invalid input. Not enough arguments."
            return str(e)
        except IndexError:
            return "Invalid input. Not enough arguments."
    return inner


def parse_input(user_input):   # Function to parse user input into command and arguments
    parts = user_input.split()
    if not parts:  # Empty input
        return "",
    cmd, *args = parts
    return cmd.lower(), *args


@input_error
def add_contact(args, book): #   Function to add a contact to the address book
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book): # Function to change a contact's phone number in the address book
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book): # Function to show a contact's phone numbers in the address book
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return f"{name}: {'; '.join(p.value for p in record.phones) or 'no phones'}"


def show_all(book): # Function to show all contacts in the address book
    if book.data:
        return "\n".join(str(record) for record in book.data.values())
    return "No contacts found."


@input_error
def add_birthday(args, book): # Function to add a birthday to a contact in the address book
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book): # Function to show a contact's birthday in the address book 
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    if record.birthday is None:
        return f"{name} has no birthday set."
    return f"{name}: {record.birthday}"


@input_error
def birthdays(args, book): # Function to show contacts with birthdays in the next 7 days
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next week."
    return "\n".join(f"{u['name']}: {u['congratulation_date']}" for u in upcoming)


def main():
    book = AddressBook() #  Create an instance of AddressBook to store contacts
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
