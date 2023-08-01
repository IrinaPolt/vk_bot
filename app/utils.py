from dataclasses import dataclass
from typing import Optional
from vktools import Keyboard, ButtonColor, Text, Carousel, Element


BUTTONS = {
    "back": "Назад",
    "check_types": "Покажите мне всё!",
    "check_cakes": "Посмотрим торты!",
    "check_ice_cream": "Как насчет мороженого?",
    "check_pastries": "Посмотрим выпечку",
    "begin": "Начать",
    "order": "Заказать",
    "finish": "Завершить заказ"
}

RESPONSES = {
    "greeting": "Привет, я бот-помощник! Начнем знакомство \
        с нашей кондитерской?",
    "types": "В нашей кондитерской можно приобрести торты, \
        мороженое и выпечку. С чего начнем?",
    "random": [
        "Девять из десяти стоматологов рекомендуют",
        "Хорошо сочетаются с чаем и кофе",
        "Жизнь слишком коротка, чтобы не есть сладкое"
    ],
    "order": "Добавлено в заказ! Посмотрим что-то еще?",
    "order_finish": "Спасибо за заказ! Мы свяжемся \
        с вами в ближайшее время. Вы заказали: ",
    "unexpected_message": "Кажется, я не готов ответить на ваш вопрос :( \
        Через некоторое время вам ответит администратор!"
}


@dataclass
class SweetItem:
    id: int
    name: str
    description: Optional[str]
    image: str
    link: str
    price: float


def make_request(message, connection):
    cur = connection.cursor()
    sql_query = ""
    if message == BUTTONS["check_cakes"]:
        sql_query = "SELECT * FROM cakes;"
    elif message == BUTTONS["check_ice_cream"]:
        sql_query = "SELECT * FROM ice_cream;"
    elif message == BUTTONS["check_pastries"]:
        sql_query = "SELECT * FROM pastries;"
    else:
        return None
    cur.execute(sql_query)
    result = cur.fetchall()
    items = [SweetItem(*row) for row in result]
    cur.close()
    return items


def create_keyboard(buttons):
    if buttons is None:
        keyboard = Keyboard([])
    else:
        buttons_kb = [Text(name, ButtonColor.POSITIVE) for name in buttons]
        if len(buttons_kb) > 1:
            buttons_kb.append(Text(BUTTONS["back"], ButtonColor.NEGATIVE))
        if len(buttons_kb) > 2:
            buttons_kb.append(Text(BUTTONS["finish"], ButtonColor.NEGATIVE))
            keyboard = Keyboard([buttons_kb[0:2], buttons_kb[2:]])
        else:
            keyboard = Keyboard([buttons_kb])
    return keyboard.add_keyboard()


def create_carousel(objs):
    if not objs:
        return None
    elements = [
        Element(
            obj.name,
            obj.description,
            obj.image,
            obj.link,
            [
                Text(BUTTONS["order"],
                     ButtonColor.POSITIVE,
                     payload={"order": obj.name})]
        ) for obj in objs]
    carousel = Carousel(elements)
    return carousel.add_carousel()
