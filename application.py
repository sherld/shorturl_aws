import uvicorn
from app import main


class application:
    @staticmethod
    def run():
        uvicorn.run(main.app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    application.run()
