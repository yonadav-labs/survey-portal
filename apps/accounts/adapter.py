from allauth.account.adapter import DefaultAccountAdapter

from .models import EmailUser

class CustomAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse

        (Comment reproduced from the overridden method.)
        """
        try:
            email = request.session.get('socialaccount_sociallogin').get('user').get('email')
            user = EmailUser.objects.filter(email=email).first()
            if user:
                user.delete()
                return True
        except Exception as e:
            pass

        return False
