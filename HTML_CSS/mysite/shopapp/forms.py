from django import forms
from django.core.exceptions import ValidationError

from .models import Product, Order


class ProductForm(forms.ModelForm):
    """
    Форма создания/редактирования продукта.
    Валидируем цену и скидку.
    """

    class Meta:
        model = Product
        # Берём самые логичные поля.
        # Если у тебя в модели другие имена — можно будет подправить,
        # но в типовом коде Skillbox они именно такие.
        fields = ["name", "description", "price", "discount"]

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_discount(self):
        discount = self.cleaned_data.get("discount")
        if discount is not None and not (0 <= discount <= 100):
            raise ValidationError("Скидка должна быть в диапазоне от 0 до 100%.")
        return discount


class OrderForm(forms.ModelForm):
    """
    Форма создания заказа.
    Предполагаем, что в модели Order есть поля:
    user, products, delivery_address, promocode (или аналогично).
    """

    class Meta:
        model = Order
        # если поля у тебя чуть отличаются — можно будет подправить список
        fields = ["user", "products", "delivery_address", "promocode"]
        widgets = {
            "products": forms.CheckboxSelectMultiple,
        }
