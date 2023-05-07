from service.settings import config_settings as cs

ascii_art = f"""
01000100 01100101 01110110 01010011 01100101 01110100 01000111 01101111                                                                              
 ______ _______    ____________________ ___________ 
 |     \|______\  / |_____|______  |   |  ___|     |
 |_____/|______ \/  ______|______  |   |_____|_____|
                                                    
http://github.com/DevSetGo

{cs.app_name.upper()}!
{cs.app_description.capitalize()}.
"""

def print_logo():
    # Split the ASCII art into multiple lines
    lines = ascii_art.split('\n')

    # Print each line of the ASCII art
    for line in lines:
        print(line)