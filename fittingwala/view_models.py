from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from typing import List
from fittingwala.models import Product, Category, SubCategory
from django.db import connection


class BaseViewModel:
    def __init__(self,
                 table: object,
                 *args,
                 **kwargs
                 ):
        pass


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
        #print logs
        print(f"Verification code for {self.email} is {self.table.objects.get(email=self.email).verification_code}")
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


class AllCombViewModel:

    def __int__(self, tables: List[object], *args, **kwargs):
        self.table = tables

    @classmethod
    def run_query(cls):
        with connection.cursor() as cursor:
            query = """
            SELECT 
                c.id AS category_id, c.name AS category_name, c.image AS category_image,
                sc.id AS subcategory_id, sc.name AS subcategory_name,
                p.id AS product_id, p.name AS product_name, p.image AS product_image,
                p.description AS product_description, p.price_map AS product_price_map,
                p.size AS product_size, p.brand AS product_brand, p.is_available AS product_available
            FROM 
                fittingwala_category c
            LEFT JOIN 
                fittingwala_subcategory sc ON c.id = sc.category_id
            LEFT JOIN 
                fittingwala_product p ON sc.id = p.subcategory_id
            ORDER BY 
                c.id, sc.id, p.id;
            """
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

            data = []
            for row in rows:
                category = {
                    'id': row[0],
                    'name': row[1],
                    'image': str(row[2]),
                    'subcategories': []
                }
                subcategory = {
                    'id': row[3],
                    'name': row[4],
                    'products': []
                }
                product = {
                    'id': row[5],
                    'name': row[6],
                    'image': str(row[7]),
                    'description': row[8],
                    'price_map': row[9],
                    'size': row[10],
                    'brand': row[11],
                    'is_available': row[12]
                }

                if not data or data[-1]['id'] != category['id']:
                    data.append(category)

                if not data[-1]['subcategories'] or data[-1]['subcategories'][-1]['id'] != subcategory['id']:
                    data[-1]['subcategories'].append(subcategory)

                if not data[-1]['subcategories'][-1]['products'] or data[-1]['subcategories'][-1]['products'][-1][
                    'id'] != product['id']:
                    data[-1]['subcategories'][-1]['products'].append(product)

            return data
