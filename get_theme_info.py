def dark_theme_details():
    detail = []
    with open('dark_info.txt', 'rt') as file:
        for line in file:
            detail.append(str(line.splitlines())[2:9])
    return detail

def light_theme_details():
    detail = []
    with open('light_info.txt', 'rt') as file:
        for line in file:
            detail.append(str(line.splitlines())[2:9])
    return detail

def default_theme_details():
    detail = []
    with open('default_info.txt', 'rt') as file:
        for line in file:
            detail.append(str(line.splitlines())[2:9])
    return detail

def colored_theme_details():
    detail = []
    with open('colored_info.txt', 'rt') as file:
        for line in file:
            detail.append(str(line.splitlines())[2:9])
    return detail

def set_last_theme(theme):
    with open('last_theme.txt', 'wt') as file:
        file.write(theme)

def get_last_theme_details():
    theme = ''
    with open('last_theme.txt', 'rt') as file:
        theme = file.read()
    return theme
