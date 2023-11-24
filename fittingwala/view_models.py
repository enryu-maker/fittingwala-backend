from django.core.mail import send_mail
from django.conf import settings
class FitUserViewModel:

    def __init__(self,
                 table: object,
                 username: str,
                 email: str,
                 password: str,
                 mobile: str,
                 is_active: bool = False,
                 *args,
                 **kwargs
                 ):
        self.username = username
        self.email = email
        self.password = password
        self.mobile = mobile
        self.is_active = is_active
        self.table = table

    def __validate(self):

        if not self.username:
            raise ValueError("Username is required")
        if not self.email:
            raise ValueError("Email is required")
        if not self.password:
            raise ValueError("Password is required")
        if not self.mobile:
            raise ValueError("Mobile is required")

    def create_user(self):
        self.__validate()
        user = self.table.objects.create_user(username=self.username, email=self.email, password=self.password,
                                              mobile=self.mobile, is_active=self.is_active)
        self.verify_user()
        return user

    def create_superuser(self):
        self.__validate()
        user = self.table.objects.create_superuser(username=self.username, email=self.email, password=self.password,
                                                   mobile=self.mobile)
        return user

    def verify_user(self):
        # send verification email
        send_mail(
            'Verify your email',
            f'Your verification code is {self.table.objects.get(email=self.email).verification_code}',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
        )


