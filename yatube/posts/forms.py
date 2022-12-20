from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = (
            'Не забываем про вдохновение 💡',
        )
        self.fields['group'].empty_label = ('В группе легче искать чем в космосе 🌌')

    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу',
        }
        help_texts = {'text': 'Текст вашего поста','group': 'Группа, к которой будет относиться пост'}
