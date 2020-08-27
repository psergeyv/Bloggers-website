from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from .models import Post, Group
import time
User = get_user_model()


class HomeWorkTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@yandex.ru", password="cl123456"
        )
        response = self.client.get("/testuser/")
        self.assertEqual(response.status_code, 200,
                         msg="Ошибка, страница пользователя не найдена!")

    def test_post_new(self):
        self.client.login(username='testuser', password='cl123456')
        response = self.client.get("/new/")
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get("/new/")
        self.assertRedirects(response, '/auth/login/?next=/new/', status_code=302,
                             target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_post_add_edit(self):
        self.client.login(username='testuser', password='cl123456')
        new_text = "Текст для теста"
        self.new = Post.objects.create(author=self.user, text=new_text)
        time.sleep(21)
        response = self.client.get("/")
        self.assertContains(response, new_text, count=None,
                            status_code=200, msg_prefix='', html=False)

        response = self.client.get(f"/{self.user.username}/")
        self.assertContains(response, new_text, count=None,
                            status_code=200, msg_prefix='', html=False)

        response = self.client.get(f"/{self.user.username}/{self.new.id}/")
        self.assertContains(response, new_text, count=None,
                            status_code=200, msg_prefix='', html=False)

        update_text = "Обновленный текст!"
        self.client.login(username='testuser', password='cl123456')
        self.new.text = update_text
        self.new.save()

        time.sleep(21)

        response = self.client.get("/")
        self.assertContains(response, update_text, count=None,
                            status_code=200, msg_prefix='', html=False)

        response = self.client.get(f"/{self.user.username}/")
        self.assertContains(response, update_text, count=None,
                            status_code=200, msg_prefix='', html=False)

        response = self.client.get(f"/{self.user.username}/{self.new.id}/")
        self.assertContains(response, update_text, count=None,
                            status_code=200, msg_prefix='', html=False)

    def test_404(self):
        response = self.client.get("/dsssmsms/")
        self.assertEqual(response.status_code, 404)

    def test_check_imd(self):
        self.client.login(username='testuser', password='cl123456')
        new_text = "Пост для проверки загрузки фото"
        image_file = 'tmp/test.jpg'

        new = Post.objects.create(
            author=self.user, text=new_text, image=image_file)
        post_id = new.id

        time.sleep(21)

        response = self.client.get("/")
        self.assertContains(response, 'img', count=None,
                            status_code=200, msg_prefix='', html=False)

        response = self.client.get(f"/{self.user.username}/{post_id}/")
        self.assertContains(response, 'img', count=None,
                            status_code=200, msg_prefix='', html=False)

        # Попробуем отредактировать запись с файлом не являющимся картинкой
        noimage_file = 'tmp/test.txt'
        with open(noimage_file, mode='rb') as fi:
            edit_post = self.client.post(
                f"/{self.user.username}/{post_id}/edit/", {'text': new_text, 'image': fi})

        self.assertEqual(response.status_code, 200)

    def test_check_change(self):
        self.client.login(username='testuser', password='cl123456')

        change_text = "Проверка change - кеширования"
        new_post = self.client.post("/new/", {'text': change_text})
        self.assertNotContains(new_post, change_text,
                               status_code=302, msg_prefix='', html=False)

        # ждем 20 секунд и проверяем, текст должен появиться, иначе что то пошло не так
        time.sleep(21)

        response = self.client.get("/")
        self.assertContains(response, change_text, count=None,
                            status_code=200, msg_prefix='', html=False)

    def test_check_follow(self):
        self.client.login(username='testuser', password='cl123456')
        check_text = 'Пост на который должен пользователь подписаться'
        self.new = Post.objects.create(author=self.user, text=check_text)

        post_id = self.new.id
        page_user = self.user.username
        follow_user = self.client.get(f"/{page_user}/follow")

        response = self.client.get(f"/{page_user}/")
        self.assertContains(response, "Отписаться", count=None,
                            status_code=200, msg_prefix='', html=False)
        response = self.client.get(f"/follow/")
        self.assertContains(response, check_text, count=None,
                            status_code=200, msg_prefix='', html=False)

        unfollow_user = self.client.get(f"/{page_user}/unfollow")
        response = self.client.get(f"/{page_user}/")
        self.assertContains(response, "Подписаться", count=None,
                            status_code=200, msg_prefix='', html=False)
        response = self.client.get(f"/follow/")
        self.assertNotContains(response, check_text,
                               status_code=200, msg_prefix='', html=False)

        response = self.client.get(f"/{page_user}/{post_id}/")
        self.assertContains(response, "Добавить комментарий",
                            count=None, status_code=200, msg_prefix='', html=False)

        self.client.logout()
        response = self.client.get(f"/{page_user}/{post_id}/")
        self.assertContains(response, "Что бы добавить комментарий, необходимо авторизироваться",
                            count=None, status_code=200, msg_prefix='', html=False)
