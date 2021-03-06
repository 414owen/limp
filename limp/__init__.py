import limp.environment as Environment
import limp.errors as Errors
import limp.tokens as Tokens
import limp.token_tree as TokenTree
import limp.types as Types
import sys


def evaluate(source_code, environment=None):
    if environment is None:
        environment = Environment.create_standard()
    return Types.Form.infer_from(
        TokenTree.create_from(
            Tokens.create_from(source_code)
        ),
        environment
    ).evaluate()


class Repl:

    PROMPT = "> "
    WELCOME_MESSAGE = f"Welcome to LIMP! You're in a REPL, have fun!\n"

    def __init__(self, input_=input, output=sys.stdout.write):
        self._input = input_
        self._output = output
        self.__displayed_welcome = False
        self.__environment = Environment.create_standard()

    def start(self):
        while True:
            self._tick()
        
    def _tick(self):
        self.__display_welcome_if_necessary()
        self.__display_prompt()
        code = self._input()
        result = self.__evaluate(code)
        self.__display_result(result)

    def __display_welcome_if_necessary(self):
        if not self.__displayed_welcome:
            self._output(Repl.WELCOME_MESSAGE)
            self.__displayed_welcome = True

    def __display_prompt(self):
        self._output(Repl.PROMPT)

    def __evaluate(self, code):
        try:
            return evaluate(code, self.__environment)
        except Errors.EmptyCode:
            pass
        except Exception as e:
            print(e.args[0], file=sys.stderr)
        return ""

    def __display_result(self, result):
        self._output(f"{result}\n")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(evaluate(open(sys.argv[1], "r").read()))
    else:
        Repl().start()
