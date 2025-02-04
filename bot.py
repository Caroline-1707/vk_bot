import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import TOKEN


class VkChatBot:
    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk_session)
        self.api = self.vk_session.get_api()
        self.greeted_users = set()

    def send_message(self, user_id, message=None, attachments=None):
        self.api.messages.send(
            user_id=user_id,
            message=message,
            attachment=','.join(attachments) if attachments else None,
            random_id=vk_api.utils.get_random_id()
        )

    def process_attachments(self, event):
        return [
            f"photo{photo['owner_id']}_{photo['id']}_{photo['access_key']}"
            for photo in event.attachments
            if event.attachments and event.attachments[0]['type'] == 'photo'
        ] if event.attachments else []

    def run(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.handle_message(event)

    def handle_message(self, event):
        user_id = event.user_id

        if user_id not in self.greeted_users:
            self.send_message(user_id, "Добро пожаловать! Отправьте мне любое изображение.")
            self.greeted_users.add(user_id)

        if attachments := self.process_attachments(event):
            self.send_message(user_id, attachments=attachments)


if __name__ == "__main__":
    bot = VkChatBot(TOKEN)
    bot.run()
