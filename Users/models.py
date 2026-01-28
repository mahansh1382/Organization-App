from django.db import models

class Authentication(models.Model):
    username=models.CharField( max_length=50)
    password=models.CharField( max_length=50)
    create_at=models.DateTimeField( auto_now_add=True)
    update_at=models.DateTimeField( auto_now=True)

    def __str__(self):
        return self.user_name



class Rols(models.Model):
    title=models.CharField( max_length=50)



class Users(models.Model):
    user_name=models.ForeignKey(Authentication, on_delete=models.CASCADE)
    first_name=models.CharField( max_length=50)
    last_name=models.CharField( max_length=50)
    mobile_number=models.IntegerField()
    national_id=models.IntegerField()
    rol_id=models.ForeignKey(Rols,on_delete=models.CASCADE)
    is_active=models.BooleanField()
    create_at=models.DateTimeField( auto_now_add=True)
    update_at=models.DateTimeField( auto_now=True)



class Provinces(models.Model):
    title=models.CharField( max_length=50)



class Cites(models.Model):
    title=models.CharField( max_length=50)



class Address(models.Model):
    full_address=models.CharField( max_length=255)
    provinc_id=models.ForeignKey(Provinces,  on_delete=models.CASCADE)
    city_id=models.ForeignKey(Cites,on_delete=models.CASCADE)



class Organization(models.Model):
    establishment_name=models.CharField( max_length=50)
    brand=models.CharField( max_length=50)
    owener_id=models.ForeignKey(Users, on_delete=models.CASCADE)
    rate=models.FloatField()
    phone_number=models.IntegerField()
    address_id=models.ForeignKey(Address, verbose_name=_(""), on_delete=models.CASCADE)
    create_at=models.DateTimeField( auto_now_add=True)
    update_at=models.DateTimeField( auto_now=True)
    org_name=models.CharField( max_length=50)



class Texts (models.Model):
    contact=models.CharField( max_length=50)
    create_at=models.DateTimeField( auto_now_add=True)
    update_at=models.DateTimeField( auto_now=True)



class Comments(models.model):
    user_id=models.ForeignKey( Users, on_delete=models.CASCADE)
    org_id=models.ForeignKey(Organization, on_delete=models.CASCADE)
    parent_id=models.IntegerField()
    text_id=models.ForeignKey(Texts, on_delete=models.CASCADE)
    is_rejected=models.BooleanField()
    is_filtered=models.BooleanField()
    rate=models.FloatField()
    create_at=models.DateTimeField( auto_now_add=True)
    update_at=models.DateTimeField( auto_now=True)
