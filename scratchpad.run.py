import code
import importlib
import readline


def run():
    importlib.reload(current)
    current.main()


def main():
    variables = globals().copy()
    variables.update(locals())
    shell = code.InteractiveConsole(variables)
    shell.interact()


if __name__ == '__main__':
    main()
