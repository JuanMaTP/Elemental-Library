from django.contrib import admin

from .models import Person

admin.site.register(Person)

'''
Allows the person info to be put together with the user info in the admin page.
Taken from Django Doc: https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#django.contrib.auth.models.CustomUser


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class PersonInline(admin.StackedInline):
    model = Person
    can_delete = False
    verbose_name_plural = 'person'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (PersonInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)'''
