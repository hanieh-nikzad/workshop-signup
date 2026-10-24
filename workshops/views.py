from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegistrationForm
from .models import Registration, Workshop
from .services import AlreadyRegistered,cancel ,register

Status = Registration.Status


def workshop_detail(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                reg = register(
                    workshop.id,
                    form.cleaned_data["name"],
                    form.cleaned_data["email"],
                )
            except AlreadyRegistered:
                form.add_error("email", "با این ایمیل قبلاً برای این کارگاه ثبت‌نام شده است.")
            else:
                if reg.status == Status.CONFIRMED:
                    messages.success(request, "ثبت‌نام شما تأیید شد.")
                else:
                    messages.warning(request, "ظرفیت پر است؛ شما در لیست انتظار قرار گرفتید.")
                return redirect("registration_status", token=reg.token)
    else:
        form = RegistrationForm()

    confirmed = workshop.registrations.filter(status=Status.CONFIRMED).count()
    context = {
        "workshop": workshop,
        "form": form,
        "confirmed": confirmed,
        "remaining": max(workshop.capacity - confirmed, 0),
    }
    return render(request, "workshops/workshop_detail.html", context)


def registration_status(request, token):
    reg = get_object_or_404(Registration, token=token)

    position = None
    if reg.status == Status.WAITLIST:
        position = Registration.objects.filter(
            workshop=reg.workshop,
            status=Status.WAITLIST,
            created_at__lt=reg.created_at,
        ).count() + 1

    return render(request, "workshops/registration_status.html", {
        "reg": reg,
        "workshop": reg.workshop,
        "position": position,
    })


def cancel_registration(request, token):
    reg = get_object_or_404(Registration, token=token)
    if request.method == "POST":
        cancel(reg.token)
        messages.success(request, "ثبت‌نام شما لغو شد.")
    return redirect("registration_status", token=reg.token)