from resources.tracker import Medicine

def main():
    '''CLI interface for interacting with the application
    '''
    app = Medicine()
    running = True

    while running:
        user_input = input("What would you like to do \n1. Check total medicine\n2. Change modifier\n3. Add medication\n4. Exit\n")

        if user_input == "":
            running = False
        else:
            user_input = int(user_input)

        match user_input:
            case 1:
                print(app)

            case 2:
                try:
                    med = input("Medication: ")
                    amount = int(input("Amount:"))
                    print(app.change_modifier(med, amount))
                except:
                    print("Invalid input")

            case 3:
                try:
                    med = input("Medication: ")
                    amount = int(input("Amount:"))
                    print(app.add_medicine(med, amount))
                except:
                    print("Invalid input")

            case 4:
                running = False


if __name__ == "__main__":
    main()