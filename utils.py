class ColorPrint:
    @staticmethod
    def green(text):
        print(f"\033[92m{text}\033[0m")  # Green

    @staticmethod
    def red(text):
        print(f"\033[91m{text}\033[0m")  # Red

    @staticmethod
    def yellow(text):
        print(f"\033[93m{text}\033[0m")  # Yellow

    @staticmethod
    def blue(text):
        print(f"\033[94m{text}\033[0m")  # Blue
