class Utils:
    @staticmethod
    def print(input: str, is_colored=True):
        rendered_line = f"\033[93m{input}\033[0m" if is_colored else input
        print("\n" + rendered_line)

    @staticmethod
    def print_list(input: list[str]):
        print()
        for item in input:
            print(f"    \u2022 \033[96m{item}\033[0m")

    @staticmethod
    def input(prompt: str) -> str:
        return input(f"\n\033[92m{prompt}\033[0m")

    @staticmethod
    def get_next_object_name(object_name: str = None) -> str:
        object_name_as_num = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(8):
            object_name_as_num[i] = ord(object_name[i]) - ord("a")

        for i in reversed(range(8)):
            if object_name_as_num[i] != 15:
                object_name_as_num[i] += 1
                break
            else:
                object_name_as_num[i] = 0

        result = [""] * 8
        for i in range(8):
            result[i] = chr(object_name_as_num[i] + ord("a"))

        return "".join(result)
