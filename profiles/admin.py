from django.contrib import admin
from profiles.profiles.models import Profile, Address, School, Membership


class ProfileAdmin(admin.ModelAdmin):
    pass


class AddressAdmin(admin.ModelAdmin):
    pass


class SchoolAdmin(admin.ModelAdmin):
    pass


class MembershipAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Membership, MembershipAdmin)
