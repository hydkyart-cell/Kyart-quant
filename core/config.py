class Config:
    APP_NAME = "Kyart Quant"
    VERSION = "0.1.0"

    AUTHOR = "Kyart"

    DEBUG = True

    LOG_LEVEL = "INFO"


if __name__ == "__main__":
    print(f"Application : {Config.APP_NAME}")
    print(f"Version     : {Config.VERSION}")
    print(f"Author      : {Config.AUTHOR}")
    print(f"Debug Mode  : {Config.DEBUG}")
    print(f"Log Level   : {Config.LOG_LEVEL}")
