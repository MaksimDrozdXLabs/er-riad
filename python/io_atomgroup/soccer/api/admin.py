from django.contrib import admin

# Register your models here.

from rest_framework.authtoken.models import Token

class TokenAdmin(admin.ModelAdmin):
    class Meta:
        model = Token

#admin.site.register(
#    Token,
#    TokenAdmin,
#)
