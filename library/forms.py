from django import forms

from .models import Book, Member


class BookForm(forms.ModelForm):
    class Meta:
        model = Book

        fields = [
            "title",
            "author",
            "isbn",
            "category",
            "total_copies",
            "available_copies",
        ]

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
        ]

class BorrowBookForm(forms.Form):

    member = forms.ModelChoiceField(
        queryset=Member.objects.all(),
        empty_label="Select a member",
    )

from django import forms

from .models import Book


class BookFilterForm(forms.Form):

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by title, author, ISBN or category...",
            }
        ),
    )

    category = forms.ChoiceField(
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    availability = forms.ChoiceField(
        required=False,
        choices=[
            ("", "All"),
            ("available", "Available"),
            ("unavailable", "Unavailable"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        categories = (
            Book.objects
            .values_list(
                "category",
                flat=True,
            )
            .distinct()
            .order_by("category")
        )

        self.fields["category"].choices = [
            ("", "All Categories"),
            *[(c, c) for c in categories],
        ]