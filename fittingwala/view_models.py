from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password


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
        self.required_fields = {
            "Username": self.username,
            "Email": self.email,
            "Password": self.password,
            "Mobile": self.mobile
        }
        self.unique_fields = {
            "Username": "username",
            "Email": "email",
            "Mobile": "mobile"
        }

    def __validate__(self):

        # loop through required fields and check if they are empty

        for field_name, field_value in self.required_fields.items():
            if not field_value:
                raise ValueError(f"{field_name} is required")

        for field_name, field_attr in self.unique_fields.items():
            if self.table.objects.filter(**{field_attr: getattr(self, field_attr)}).exists():
                self.verify_user()
                raise ValueError(f"{field_name} already exists")

    def create_user(self):

        # validate fields
        self.__validate__()

        # create user
        user = self.table.objects.create_user(username=self.username, email=self.email,
                                              mobile=self.mobile)
        user.set_password(self.password)
        user.save()
        self.verify_user()
        return user

    def create_superuser(self):
        # validate fields
        self.__validate__()

        # create superuser
        user = self.table.objects.create_superuser(username=self.username, email=self.email, password=self.password,
                                                   mobile=self.mobile)
        return user

    def verify_user(self):
        # send verification email
        try:
            send_mail(
                'Verify your email',
                f'Your verification code is {self.table.objects.get(email=self.email).verification_code}',
                settings.EMAIL_HOST_USER,
                [self.email],
                fail_silently=False,
            )
        except Exception as e:
            print(e)
        return
