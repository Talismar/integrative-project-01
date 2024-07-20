from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView

from sacm_pi_1.clinic.forms import DoctorChangeForm

User = get_user_model()


class UserLoginView(LoginView):
    template_name = "account/login.html"

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


user_login_view = UserLoginView.as_view()


class UserLogoutView(LogoutView):

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


user_logout_view = UserLogoutView.as_view()


class UpdateProfileView(UpdateView):

    def form_valid(self, form):
        context = self.get_context_data()
        # print(form)
        try:
            password_change_form = context["password_form"]
            if password_change_form.is_valid() and form.is_valid():
                form.save()

                is_authenticated = password_change_form.user.is_authenticated

                password_change_form.save()

                """
                    Fazendo login do usuario novamente caso esteja mudando do seu perfil
                """
                update_session_auth_hash(self.request, password_change_form.user)

                return redirect(self.get_success_url())

        except KeyError:
            if form.is_valid():
                form.save()

                if type(form) == DoctorChangeForm:

                    speciality = Speciality.objects.get(
                        pk=self.request.POST.get("speciality")
                    )
                    update_Doctor = Doctor.objects.get(pk=self.request.user.pk)
                    update_Doctor.crm = self.request.POST.get("crm")
                    update_Doctor.speciality = speciality
                    update_Doctor.save()

                return redirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["form"] = self.form_class(
                self.request.POST, self.request.FILES, instance=self.request.user
            )

            password_post = {
                "old_password": self.request.POST.get("old_password"),
                "new_password1": self.request.POST.get("new_password1"),
                "new_password2": self.request.POST.get("new_password2"),
            }
            # print(self.request.POST, self.request.FILES)
            if password_post["old_password"]:
                # print("Password")
                context["password_form"] = self.password_form_class(
                    user=self.request.user, data=password_post
                )

        else:
            context["password_form"] = self.password_form_class(user=self.request.user)

        return context
