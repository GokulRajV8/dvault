import getpass

from . import Constants


class Utils:
    @staticmethod
    def print(message: str, is_colored=True):
        print(
            "\n" + f"{Constants.COLOR_CLI_MESSAGE}{message}{Constants.COLOR_CLI_END}"
            if is_colored
            else message
        )

    @staticmethod
    def print_list(input: list[str]):
        print()
        for item in input:
            print(
                " " * Constants.INTEND_CLI_LIST
                + f"{Constants.BULLET_CLI_LIST} {Constants.COLOR_CLI_LIST}{item}{Constants.COLOR_CLI_END}"
            )

    @staticmethod
    def input(prompt: str) -> str:
        return input(
            "\n" + f"{Constants.COLOR_CLI_INPUT}{prompt}{Constants.COLOR_CLI_END}"
        )

    @staticmethod
    def input_password(prompt: str) -> str:
        return getpass.getpass(
            f"{Constants.COLOR_CLI_INPUT}{prompt}{Constants.COLOR_CLI_END}"
        )

    @staticmethod
    def get_next_object_name(object_name: str = None) -> str:
        if object_name is None:
            return Constants.OBJ_NAME_CHAR_START * Constants.OBJ_NAME_LEN

        object_name_as_num = [0] * Constants.OBJ_NAME_LEN
        for i in range(Constants.OBJ_NAME_LEN):
            object_name_as_num[i] = ord(object_name[i]) - ord(
                Constants.OBJ_NAME_CHAR_START
            )

        for i in reversed(range(Constants.OBJ_NAME_LEN)):
            if object_name_as_num[i] != Constants.OBJ_NAME_CHAR_COUNT:
                object_name_as_num[i] += 1
                break
            else:
                object_name_as_num[i] = 0

        result = [""] * Constants.OBJ_NAME_LEN
        for i in range(Constants.OBJ_NAME_LEN):
            result[i] = chr(object_name_as_num[i] + ord(Constants.OBJ_NAME_CHAR_START))

        return "".join(result)
