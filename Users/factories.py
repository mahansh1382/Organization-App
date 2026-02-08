import random
import factory
from factory.django import DjangoModelFactory
# مدل‌ها از طریق پکیج محلی وارد می‌شوند (باید در محیط واقعی تنظیم شود)
# برای سادگی، ما فرض می‌کنیم که مدل‌ها در جایی که این فکتوری‌ها اجرا می‌شوند قابل دسترسی هستند.
# از آنجایی که شما مدل‌ها را ارائه دادید، ما باید از ساختار آن‌ها استفاده کنیم:
try:
    from .models import Authentication, Rols, Users, Provinces, Cites, Address, Organization, Texts, Comments
except ImportError:
    # در صورت اجرای مستقیم، ممکن است نیاز به تعریف دستی مدل‌ها باشد، اما در محیط واقعی Django
    # این کار به صورت خودکار انجام می‌شود. ما ادامه می‌دهیم با فرض وجود این مدل‌ها.
    pass 


# -------------------------
# Authentication Factory
# -------------------------
class AuthenticationFactory(DjangoModelFactory):
    class Meta:
        model = Authentication # استفاده مستقیم از نام کلاس مدل

    # فیلد مدل: username (CharField)
    username = factory.Faker("user_name") # استفاده از فرمت‌دهنده درست
    password = factory.Faker("password")

    def __str__(self):
        # اصلاح: مدل شما در اینجا user_name را برمی‌گرداند، اما فیلد در این مدل username است.
        # من username را برمی‌گردانم تا با فیلد تعریف شده مطابقت داشته باشد.
        return self.username 


# -------------------------
# Rols Factory
# -------------------------
class RolsFactory(DjangoModelFactory):
    class Meta:
        model = Rols

    title = factory.Iterator(["admin", "user", "manager"])


# -------------------------
# Users Factory
# -------------------------
class UsersFactory(DjangoModelFactory):
    class Meta:
        model = Users

    # مدل: user_name=models.ForeignKey(Authentication, ...)
    # SubFactory به صورت خودکار کلید خارجی را با ID شیء تولید شده پر می‌کند.
    user_name = factory.SubFactory(AuthenticationFactory) 
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    mobile_number = factory.LazyFunction(lambda: random.randint(9000000000, 9999999999))
    national_id = factory.LazyFunction(lambda: random.randint(1000000000, 9999999999))
    rol_id = factory.SubFactory(RolsFactory) 
    
    # مدل: is_active=models.BooleanField()
    is_active = factory.LazyFunction(lambda: random.choices([True, False], weights=[20, 80], k=1)[0]) 


# -------------------------
# Provinces Factory
# -------------------------
class ProvincesFactory(DjangoModelFactory):
    class Meta:
        model = Provinces
    title = factory.Faker("state")


# -------------------------
# Cites Factory
# -------------------------
class CitesFactory(DjangoModelFactory):
    class Meta:
        model = Cites
    title = factory.Faker("city")


# -------------------------
# Address Factory
# -------------------------
class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address
    full_address=factory.Faker("address")
    provinc_id = factory.SubFactory(ProvincesFactory)
    city_id = factory.SubFactory(CitesFactory)


# -------------------------
# Organization Factory
# -------------------------
class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    establishment_name=factory.Faker("company")
    brand=factory.Faker("company_suffix")
    # مدل: owener_id=models.ForeignKey(Users, ...) - دقیقاً مطابقت دارد
    owener_id = factory.SubFactory(UsersFactory) 
    rate=factory.LazyFunction(lambda: round(random.uniform(1.0, 5.0), 1))
    phone_number=factory.LazyFunction(lambda: random.randint(9000000000, 9999999999))
    # مدل: address_id=models.ForeignKey(Address, ...) - دقیقاً مطابقت دارد
    address_id = factory.SubFactory(AddressFactory) 
    org_name=factory.Faker("company")


# -------------------------
# Texts Factory
# -------------------------
class TextsFactory(DjangoModelFactory):
    class Meta:
        model = Texts
    contact=factory.Faker("sentence", nb_words=10)


# -------------------------
# Comments Factory
# -------------------------
class CommentsFactory(DjangoModelFactory):
    class Meta:
        model = Comments

    # مدل: user_id=models.ForeignKey(Users, ...)
    user_id = factory.SubFactory(UsersFactory)
    # مدل: org_id=models.ForeignKey(Organization, ...)
    org_id = factory.SubFactory(OrganizationFactory)
    parent_id=0 # مقدار ثابت
    # مدل: text_id=models.ForeignKey(Texts, ...)
    text_id = factory.SubFactory(TextsFactory) 
    is_rejected = factory.LazyFunction(lambda: random.choice([True, False]))
    is_filtered = factory.LazyFunction(lambda: random.choice([True, False]))
    rate = factory.LazyFunction(lambda: round(random.uniform(1.0, 5.0), 1))
