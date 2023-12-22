from django import forms

from catalog.models import ContactData, Product, Version

bad_words = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар')


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ContactDataForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = ContactData
        #fields = '__all__'
        fields = ('name', 'phone', 'message',)


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ('name', 'description', 'image', 'category', 'price',)

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        if cleaned_data.lower() in bad_words:
            raise forms.ValidationError('Ошибка, запрещенное имя!')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        if cleaned_data.lower() in bad_words:
            raise forms.ValidationError('Ошибка, запретная тема!')
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ('product', 'number', 'name', 'is_active',)

    def clean_is_active(self):
        cleaned_data = self.cleaned_data.get('is_active')
        #print(self.__dict__)
        if cleaned_data:
            version = self.cleaned_data['product'].version_set.filter(is_active=True)
            if version:
                raise forms.ValidationError('Ошибка, у продукта уже есть активная версия!')
                #for vers in version:   #  это вариант с удалением активности остальных версий
                #    vers.is_active = False  #  при включении новой активной версии
                #    vers.save()
        return cleaned_data



