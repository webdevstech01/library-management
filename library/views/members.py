from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import MemberForm
from ..models import Member
from django.urls import reverse

@staff_member_required
def members(request):
    members = Member.objects.all()

    return render(
        request,
        "library/member_list.html",
        {
            "members": members,
        },
    )

@staff_member_required
def add_member(request):

    if request.method == "POST":

        form = MemberForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("members")

    else:

        form = MemberForm()

    return render(
        request,
        "library/form.html",
        {
            "form": form,
            "title": "Adauga membru",
            "cancel_url": reverse("members"),
        },
    )


@staff_member_required
def edit_member(request, member_id):

    member = get_object_or_404(
        Member,
        id=member_id,
    )

    if request.method == "POST":

        form = MemberForm(
            request.POST,
            instance=member,
        )

        if form.is_valid():

            form.save()

            return redirect("members")

    else:

        form = MemberForm(
            instance=member,
        )

    return render(
        request,
        "library/form.html",
        {
            "form": form,
            "title": "Editeaza membru",
            "cancel_url": reverse("members"),
        },
    )

@staff_member_required
def delete_member(request, member_id):

    member = get_object_or_404(
        Member,
        id=member_id,
    )

    if request.method == "POST":

        try:

            member.delete()

            messages.success(
                request,
                "Member deleted successfully.",
            )

        except ProtectedError:

            messages.error(
                request,
                "Cannot delete this member because they have loan history.",
            )

        return redirect("members")

    return render(
        request,
        "library/member_confirm_delete.html",
        {
            "member": member,
        },
    )
