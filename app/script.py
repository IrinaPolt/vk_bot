import psycopg2
from time import sleep
from envreader import EnvReader, Field
from vk_api.longpoll import VkLongPoll, VkEventType

from fsm import VkBot


class Config(EnvReader):
    DB_HOST: str = Field(..., description="DB host")
    DB_PORT: int = Field(..., description="DB port")
    POSTGRES_USER: str = Field(..., description="DB user")
    POSTGRES_PASSWORD: str = Field(..., description="DB password")
    POSTGRES_DB: str = Field(..., description="DB name")
    VK_TOKEN: str = Field(..., description="VK token")


def main():

    cfg = Config()
    sleep(10)
    try:
        connection = psycopg2.connect(
            user=cfg.POSTGRES_USER,
            password=cfg.POSTGRES_PASSWORD,
            host=cfg.DB_HOST,
            port=cfg.DB_PORT,
            database=cfg.POSTGRES_DB
        )
        print("Соединение установлено!")
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при подключении:", error)

    token = cfg.VK_TOKEN

    bot = VkBot(token)

    longpoll = VkLongPoll(bot.vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            text = event.text
            bot.handle_message(user_id, text, connection, event.extra_values)

    connection.close()


if __name__ == '__main__':
    main()
