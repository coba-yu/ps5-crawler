import os
import requests


class LineNotifier:
    __ACCESS_TOKEN = os.environ["LINE_NOTIFY_ACCESS_TOKEN"]
    __POST_URL = "https://notify-api.line.me/api/notify"

    @classmethod
    def notify(cls, message: str, **kwargs) -> None:
        response = requests.post(
            url=cls.__POST_URL,
            data=dict(message=message),
            headers=dict(Authorization=f"Bearer {cls.__ACCESS_TOKEN}"),
            **kwargs
        )
        response.raise_for_status()


if __name__ == '__main__':
    LineNotifier.notify(message="test")
