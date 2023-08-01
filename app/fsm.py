import json
import random
import vk_api
from vk_api.utils import get_random_id
from transitions import Machine

from utils import (
    BUTTONS,
    make_request,
    create_keyboard,
    create_carousel,
    RESPONSES
)


class VkBot(object):
    states = ['meet and greet', 'choose type', 'choose product', 'order']

    def __init__(self, token):

        self.vk_session = vk_api.VkApi(token=token)
        self.vk_api = self.vk_session.get_api()

        self.order = []

        self.machine = Machine(
            model=self, states=VkBot.states, initial='meet and greet')
        self.machine.add_ordered_transitions()

        self.machine.add_transition(
            trigger='beginning', source='*', dest='meet and greet')

    def to_previous_state(self):
        states = VkBot.states
        index = states.index(self.state)
        self.machine.set_state(states[index - 1])

    def handle_message(self, user_id, message, connection, payload=None):
        if message == "Назад":
            self.to_previous_state()

        if message == "Завершить заказ":
            response = RESPONSES["order_finish"] + ", ".join(self.order)
            self.vk_api.messages.send(
                user_id=user_id,
                message=response,
                random_id=get_random_id(),
                keyboard=create_keyboard(None))
            self.beginning()
            return

        if message == "Заказать":
            data = json.loads(payload["payload"])
            self.order.append(data["order"])
            response = RESPONSES["order"]
            self.vk_api.messages.send(
                user_id=user_id, message=response, random_id=get_random_id())
            return

        if (message not in BUTTONS.values() and
                message not in RESPONSES.values()):
            response = RESPONSES["unexpected_message"]
            self.vk_api.messages.send(
                user_id=user_id,
                message=response,
                random_id=get_random_id(),
                keyboard=create_keyboard(None))
            self.beginning()

        elif self.state == "meet and greet":
            response = RESPONSES["greeting"]
            buttons = [BUTTONS["check_types"], ]
            self.vk_api.messages.send(
                user_id=user_id,
                message=response,
                random_id=get_random_id(),
                keyboard=create_keyboard(buttons)
            )
            self.next_state()

        elif self.state == 'choose type':
            response = RESPONSES["types"]
            buttons = [
                BUTTONS["check_cakes"],
                BUTTONS["check_ice_cream"],
                BUTTONS["check_pastries"]
            ]
            self.vk_api.messages.send(
                user_id=user_id,
                message=response,
                random_id=get_random_id(),
                keyboard=create_keyboard(buttons),
            )
            self.next_state()

        elif self.state == 'choose product':
            data = make_request(message, connection)
            if not data:
                response = RESPONSES["order"]
            else:
                response = random.choice(RESPONSES["random"])
            self.vk_api.messages.send(
                user_id=user_id,
                message=response,
                random_id=get_random_id(),
                template=create_carousel(data))
