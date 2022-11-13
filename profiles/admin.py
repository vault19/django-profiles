from django.contrib import admin
from profiles.models import Profile, Address, School, Membership


class ProfileAdmin(admin.ModelAdmin):
    pass


class AddressAdmin(admin.ModelAdmin):
    pass


class SchoolAdmin(admin.ModelAdmin):
    search_fields = ['school_code', 'address__street', 'address__city', 'name']
    list_display = ('name', 'address', 'school_code', 'members_count')

    def members_count(self, obj):
        return obj.members.all().count()


class MembershipAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Membership, MembershipAdmin)
