from django import forms
from .models import Group, Post, Comment


class PostForm(forms.ModelForm):

    def clean_text(self):

        cleaned_data = self.clean()
        text_validate = cleaned_data.get('text')
        duplicate_text = Post.objects.filter(text__contains=text_validate)
        if duplicate_text.count() > 1:
            self.add_error('text', f"Вы уже опубликовали похожий текст!")

        if len(text_validate) < 20:
            self.add_error('text', "Слишком мало текста для публикации!")

        return text_validate

    class Meta:
        model = Post
        fields = ["group", "text", "image"]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["text"]
