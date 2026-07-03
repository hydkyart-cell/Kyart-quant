from pathlib import Path


class FileManager:

    @staticmethod
    def ensure_directory(path):
        Path(path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def write_text(path, text):
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)

    @staticmethod
    def read_text(path):
        with open(path, "r", encoding="utf-8") as file:
            return file.read()


if __name__ == "__main__":
    FileManager.ensure_directory("../data")

    FileManager.write_text(
        "../data/test.txt",
        "Kyart Quant Foundation Engine"
    )

    print(FileManager.read_text("../data/test.txt"))
