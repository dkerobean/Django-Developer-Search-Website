from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','email','username', 'password1','password2']
        labels = {
            'first_name': 'Name',
        }


    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','email','username', 'location',
                    'bio', 'short_intro', 'profile_image',
                    'social_github','social_linkedin', 'social_twitter','social_youtube', 'social_website' ]


    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class AddSkill(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(AddSkill, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SendMessage(ModelForm):
    class Meta:
        model = Message
        fields = ['name','email','subject','body']

    def __init__(self, *args, **kwargs):
        super(SendMessage, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
