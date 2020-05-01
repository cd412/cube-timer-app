def salt_password(password):
    # for every 2 characters insert "$J*"
    password_array = []
    for i, char in enumerate(password):
        password_array.append(char)
        if (i+1) % 2 == 0:
            password_array.append('$J*')
    return ''.join(password_array)

