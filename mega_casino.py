""" Mega Casino Game Implementation"""
from random import randint


class User:

    def __init__(self, name, money):
        if money < 0:
            raise Exception("Enter not minus value")
        self.name = name
        self._money = money

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, money):
        if money < 0:
            raise Exception("Enter not minus value")
        self._money = money

    def play(self, money):
        for index, machine in enumerate(Casino.game_machines):
            print("available money {} in game machine {}".format(machine.money, index))
        # find out if game machines with 3x possibility win exist
        machines_with_enough_money = [machine for machine in Casino.game_machines if machine.money >= money * 3]

        if len(machines_with_enough_money) == 0:
            print("There are no machines with enough money for game (for possible 3x won), decrease the sum")
        else:
            money_won, generated_value = machines_with_enough_money[0].play(money)
            print(
                "generated value is {}  (for possible 3x won 3 common digits, for 2x won 2 common digits or you lose)".format(
                    generated_value))
            self.money = self.money + money_won
        return


class SuperAdmin(User):
    casino = None

    def __init__(self, name, money):
        super().__init__(name, money)

    def create_casino(self, name):
        if self.casino is None:
            self.casino = Casino(name)
        else:
            # recreate casino, add money from game machines to admin total money, clear previously existed game machines
            self.money = self.money + sum(machine.money for machine in self.casino.game_machines)
            self.casino.game_machines.clear()
            self.casino = Casino(name)
            print("Recreate")

    def create_game_machine(self, money):
        if self.money < money:
            raise Exception("Super Admin has only {} money".format(self.money))
        self.money = self.money - money
        self.casino.game_machines.append(GameMachine(money))

    def withdraw_money(self, number):
        # get money from machines
        available_money_on_machines = sum(machine.money for machine in self.casino.game_machines)
        if available_money_on_machines < number:
            raise Exception(
                "Not enough money there are only {} money on game machines".format(available_money_on_machines))
        self.money = self.money + number
        for machine in sorted(self.casino.game_machines, key=lambda machine: machine.money, reverse=True):
            if machine.money > number:
                machine.money = machine.money - number
                break
            number = number - machine.money
            machine.money = 0


    def add_money(self, index, money):
        # add money to concrete game machine of casino
        if self.money >= money:
            self.casino.game_machines[index].add_money(money)
            self.money = self.money - money
        else:
            raise Exception("Not enough money you have {}".format(self.money))

    def delete_game_machine(self, index):
        # delete concrete game machine and divide its money between others
        money = self.casino.game_machines[index].money
        del self.casino.game_machines[index]
        count = len(self.casino.game_machines)
        if count == 0:
            self.money = self.money + money
            return
        on_machine = money / count
        for machine in self.casino.game_machines:
            machine.money = machine.money + on_machine


class Casino:
    game_machines = []

    def __init__(self, name):
        self.name = name

    # get total money sum of Casino
    @property
    def money(self):
        return sum(machine.money for machine in self.game_machines)

    def get_machine_count(self):
        return len(self.game_machines)


class GameMachine:
    def __init__(self, number):
        if number < 0:
            raise Exception("Enter not minus value")
        self._number = number

    # get total money sum of game machine
    @property
    def money(self):
        return self._number

    @money.setter
    def money(self, money):
        if money < 0:
            raise Exception("Enter not minus value")
        self._number = money

    def withdraw_money(self, number):
        self.money = self.money - number

    def add_money(self, number):
        self.money = self.money + number

    def play(self, number):
        generated_value = randint(100, 999)
        unique_numbers = len(set(str(generated_value)))
        if unique_numbers == 1:
            self.money = self.money - number * 3
            return number * 3, generated_value
        if unique_numbers == 2:
            self.money = self.money - number * 2
            return number * 2, generated_value
        if unique_numbers == 3:
            self.money = self.money + number
            return -number, generated_value


if __name__ == "__main__":
    users = []
    super_admin = None
    while True:
        try:
            choice = int(
                input("0. Exit 1. Create User 2. Create Super Admin 3. Create Casino 4. Create Game Machine 5. Play \n"
                      " 6. Add money to account 7. Add money to Game Machine "
                      "8. Withdraw money from Game Machine 9. Delete game machine 10. Info: "))
            if choice == 0:
                break
            elif choice == 1:
                name = input("Enter user name: ")
                if any(user.name == name for user in users):
                    print("User with the same name was already created")
                    continue
                money = float(input("Enter user money: "))
                users.append(User(name, money))
            elif choice == 2:
                if super_admin is None:
                    name = input("Enter Super Admin name: ")
                    money = float(input("Enter Super Admin money: "))
                    super_admin = SuperAdmin(name, money)
                else:
                    choice = input("Do you want recreate admin type yes or no: ")
                    if choice == "yes":
                        name = input("Enter Super Admin name: ")
                        money = float(input("Enter Super Admin money: "))
                        super_admin = SuperAdmin(name, money)
                        Casino.game_machines.clear()
                    else:
                        continue
            elif choice == 3:
                if super_admin:
                    if super_admin.casino is None:
                        name = input("Enter Casino Name: ")
                        super_admin.create_casino(name)
                    else:
                        choice = input("recreate Casino type yes or no: ")
                        if choice == "yes":
                            name = input("Enter Casino Name: ")
                            super_admin.create_casino(name)
                        else:
                            continue
                else:
                    print("Create Super Admin to create Casino")
                    continue
            elif choice == 4:
                if super_admin and super_admin.casino:
                    money = float(input("Enter money count to initialize new machine: "))
                    super_admin.create_game_machine(money)
                else:
                    print("Create Super Admin and/or Casino")
                    continue
            elif choice == 5:
                for index, user in enumerate(users):
                    print("index {} name {} money {}".format(index, user.name, user.money))
                user_index = int(input("Select user index number to play: "))
                money = float(input("Enter money count to play: "))
                users[user_index].play(money)
                print("The balance of user {} is {} ".format(users[user_index].name, users[user_index].money))
            elif choice == 6:
                add_money = input("Add money to Admin type a or to one of simple users type u: ")
                if add_money == "a" and super_admin:
                    value = float(input("How much money to add? : "))
                    super_admin.money = super_admin.money + value
                    print("The balance of super admin {} is {} ".format(super_admin.name, super_admin.money))
                elif add_money == "u":
                    for index, user in enumerate(users):
                        print("index {} name {} money {}".format(index, user.name, user.money))
                    user_index = int(input("Select user index number to add: "))
                    value = float(input("How much money to add? :"))
                    users[user_index].money = users[user_index].money + value
                    print("The balance of user {} is {} ".format(users[user_index].name, users[user_index].money))
            elif choice == 7 and super_admin:
                for index, machine in enumerate(super_admin.casino.game_machines):
                    print("Machine with {} index has {} money ".format(index, machine.money))
                index = int(input("Type index of machine to add money: "))
                how_much = float(input("Type how much to add: "))
                super_admin.add_money(index, how_much)
            elif choice == 8 and super_admin:
                for index, machine in enumerate(super_admin.casino.game_machines):
                    print("Machine with {} index has {} money ".format(index, machine.money))
                how_much = float(input("Type how much to withdraw: "))
                super_admin.withdraw_money(how_much)
            elif choice == 9:
                if super_admin and super_admin.casino:
                    machine_count = super_admin.casino.get_machine_count()
                    print("There is ' {} ' casino and game machines available".format(super_admin.casino.name,
                                                                                      machine_count))
                    for index, machine in enumerate(super_admin.casino.game_machines):
                        print("Machine with {} index has {} money ".format(index, machine.money))

                    if machine_count > 1:
                        index = int(input("Enter game machine index to delete: "))
                        super_admin.delete_game_machine(index)
                    elif machine_count == 0:
                        continue
                    else:
                        print("There is just one machine, there no machines to divide between")
            elif choice == 10:
                for index, user in enumerate(users):
                    print("user {} {} has {} money".format(index, user.name, user.money))
                if super_admin and super_admin.casino:
                    print("super admin {} has {} money".format(super_admin.name, super_admin.money))
                    print("There is ' {} ' casino and {} game machines available".format(super_admin.casino.name,
                                                                                         super_admin.casino.get_machine_count()))
                    for index, machine in enumerate(super_admin.casino.game_machines):
                        print("Machine with {} index has {} money ".format(index, machine.money))
            else:
                continue
        except Exception as e:
            print(e)
