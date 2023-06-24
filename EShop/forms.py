from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from EShop.models import BuyerUser, Product, ProductImage, Tag


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("developer", "popularity", "approved",)
        labels = {
            'descriptionImage': ('Game Page Image'),
            'longDescription': ('Long Description'),
            'titleImage': ('Title Image'),

        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control mb-3"

            if field.widget_type == "checkbox":
                field.field.widget.attrs["class"] = "form-check-input float-end mb-5"


ImageFormSet = inlineformset_factory(Product, ProductImage, fields=['image'], extra=1, can_delete=False)


class BuyerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BuyerForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=100)
    repeat_password = forms.CharField(max_length=100)

    def clean(self):

        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        repeatedPassword = self.cleaned_data.get("repeat_password")

        if None in [username, email, password, repeatedPassword]:
            raise ValidationError("Fill every input")

        if User.objects.filter(username=username).exists():
            self.add_error("username", "Username already exists")
            raise ValidationError("Username already exists")

        if User.objects.filter(email=email.lower()).exists():
            self.add_error("email", "Email already exists")
            raise ValidationError("Email already exists")

        if password != repeatedPassword:
            self.add_error("password", "Passwords need to match")
            self.add_error("repeat_password", "Passwords need to match")

            raise ValidationError("Passwords are not matching")

        return self.cleaned_data


class UserPictureUpdateForm(forms.ModelForm):
    class Meta:
        model = BuyerUser
        fields = ["profilePicture", ]


class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control my-3"

    class Meta:
        model = Tag
        fields = ["name"]
        labels = {"name": "Внеси нов таг"}
