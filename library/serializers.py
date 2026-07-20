from rest_framework import serializers

from .models import Book, Member, Loan


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"

class BorrowBookSerializer(serializers.Serializer):
    member_id = serializers.IntegerField()
    book_id = serializers.IntegerField()

class ReturnBookSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField()

class LoanSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    member = MemberSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = "__all__"