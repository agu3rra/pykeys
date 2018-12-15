def numeric_menu(options):
    """
    Asks the user for numeric input based on an input dictionary of options.

    :param options: (dict) a numerical selection menu.
                    E.g.: {1: 'Do this',
                           2: 'Do that'}
    """
    if type(options) != dict: 
        raise TypeError('numeric_menu requires a dictionary as input')

    while True:
        print('Please select one of the options below:')
        for _, value in options.items():
            print(value)
        user_selection = input()
        user_selection = int(user_selection)
        if user_selection in options.keys():
            return user_selection