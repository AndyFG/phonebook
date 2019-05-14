import os


class Phone:
    def __init__(self, name, number, outgoing):
        self.name = name  # if this was persisting in a DB must have an index according to task description
        self.number = number
        self.outgoing = outgoing

    def __repr__(self):
        return "%s: %s (%s outgoing calls)" % (self.name, self.number, self.outgoing)

    def __str__(self):
        return self.__repr__()


class Phonebook:
    def __init__(self):
        self.phonebook = {}
        self.phonebook_file = 'phonebook.txt'

    def load(self):
        self.phonebook.clear()

        file = open(self.phonebook_file, 'r')
        for line in file.readlines():
            if line.strip():
                name, number, outgoing = line.strip().split('::')
                self.phonebook[number] = Phone(name, number, outgoing)
        file.close()

    @staticmethod
    def __check__(number):
        response = True

        try:
            if number[0] == '+' and number[4:6] in ['87', '88', '89'] and 2 <= int(number[6]) <= 9:
                if len(number[7:]) == 6:
                    for digit in number[7:]:
                        if 0 >= int(digit) >= 9:
                            response = False
                            break
                else:
                    response = False
            else:
                response = False
        except:
            response = False

        return response

    def from_file(self):
        imported = {}
        excluded = {}

        self.load()

        filename = input("Enter filename location: ")
        file = open(self.phonebook_file, 'a')
        import_file = open(str(filename), 'r')

        for line in import_file.readlines():
            name, number = line.strip().split(',')

            if number[0:2] == '08':
                number = '+359' + number[1:]
            elif number[0:5] == '00359':
                number = '+' + number[2:]

            if self.__check__(number):
                imported[name] = number
                existing = self.phonebook.get(number, False)

                if not existing:
                    file.write(name + '::' + number + '::0\n')
            else:
                excluded[name] = number

        print('Phone numbers recorded: ', imported)
        print('Phone numbers excluded: ', excluded)

        import_file.close()
        file.close()

    def add(self):
        self.load()

        name = input("Enter Name: ")
        number = input("Enter Number: ")
        existing = self.phonebook.get(number, False)

        if not existing:
            if name and number and self.__check__(number):
                file = open(self.phonebook_file, 'a')
                file.write(name + '::' + number + '::0\n')
                file.close()
            else:
                print('Values cannot be empty and phone number must be like +359 87 8 123456')
        else:
            print('The number already exists associated to %s' % existing)

    def read(self):
        def sort_by(elem):
            return elem[1].name

        self.load()

        phones = list(self.phonebook.items())
        phones.sort(key=sort_by)

        for phone in phones:
            print(phone[1])
        if len(self.phonebook) == 0:
            print("Phone book is empty")

    def top(self):
        def sort_by(elem):
            return elem[1].outgoing

        self.load()

        phones = list(self.phonebook.items())
        phones.sort(key=sort_by, reverse=True)

        for phone in phones[0:5]:
            print(phone[1])
        if len(self.phonebook) == 0:
            print("Phone book is empty")

    def search(self):
        self.load()

        search = input("Enter name to search for: ")
        found = False

        if search:
            for phone in self.phonebook.values():
                if phone.name == search:
                    print(phone)
                    found = True
                    break

            if not found:
                print('Record not found')
        else:
            print('Value cannot be empty')

    def delete(self):
        self.load()

        name = input("Enter the name you want to delete: ")
        found = False

        if name:
            shadow = dict(self.phonebook)

            for phone in self.phonebook.values():
                if phone.name == name:
                    shadow = dict(self.phonebook)
                    del shadow[phone.number]
                    found = True

            if found:
                self.phonebook = shadow
                file = open(self.phonebook_file, 'w')

                for phone in self.phonebook.values():
                    string = phone.name + '::' + phone.number + '::' + phone.outgoing + '\n'
                    file.write(string)

                file.close()
                print("Record deleted successfully")

            else:
                print('Record not found')
        else:
            print('Value cannot be empty')

    @staticmethod
    def exit():
        os.abort()

    def menu(self):
        print("""
                -MENU-
                1) Print order by name
                2) Add phone number
                3) Delete phone number
                4) Search by name
                5) Import from file
                6) Print top five numbers by outgoing calls
                7) Exit
                """)

        choice = input("Type Choice: ")

        choice_menu = {
            '1': self.read,
            '2': self.add,
            '3': self.delete,
            '4': self.search,
            '5': self.from_file,
            '6': self.top,
            '7': self.exit
        }

        # try:
        choice_menu[choice]()
        # except:
        #     print("PLEASE ENTER A VALID CHOICE")


if __name__ == "__main__":
    pbook = Phonebook()
    pbook.menu()
