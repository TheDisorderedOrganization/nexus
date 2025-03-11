from colorama import Fore, Style

"""
Module: print_title
-------------------

This module provides a function to print the title and version of the package.

Functions:
----------
    - print_title: Prints the title and the version of the package.
"""

def print_title(__version__) -> None:
    """
    Prints the title and the version of the package.

    Parameters:
    -----------
        __version__ (str): The version of the package.

    Returns:
    --------
        None
    """
    title = Fore.LIGHTBLUE_EX + r"""
                                                                
    :-:      --:   -=+++=-  -:     ==: ::       :-:    :+*##*=: 
   *@@%#-   +@@# -%@@@@@@@=*@%*: :#@@+=@@+     -@@%:  =@@@@@@@+ 
  -@@@@@@+  #@@%:%@@%+==== -%@@@#%@@#:+@@#     =@@@-  %@@%--=-  
  =@@@@@@@= #@@#-@@@%+=-    :*@@@@@+  +@@%:    +@@@-  +@@@@%#*: 
  =@@@=#@@@#@@@+=@@@@@@*      #@@@#   =@@@=    *@@%:   -+#%@@@%-
  =@@% :%@@@@@@==@@@*--     :*@@@@@#: :%@@@*==*@@@+ -##+  :#@@@+
  =@@%  -%@@@@# :@@@#*###*:-%@@@#%@@@- -%@@@@@@@@*  *@@@#*#@@@@-
  -%%+   :+##+:  =%@@@@@@%:=@@%- :#%%-  :+#%%%%*-   :%@@@@@@@#= 
    :              :-----:  :-     :       :::        -=+++=:   
    """ + Style.RESET_ALL
    print(title)
    print(f"__version__ \u279c  {__version__}\n")
    return
