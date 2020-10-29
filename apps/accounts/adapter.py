from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .models import EmailUser

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_auto_signup_allowed(self, request, sociallogin):
        auto_signup = False
        email = getattr(sociallogin.user, "email")
        # Let's check if auto_signup is really possible...
        if email:
            user = EmailUser.objects.filter(email=email).first()
            if user:
                user.delete()
                auto_signup = True

        return auto_signup
