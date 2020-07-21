from django.contrib import admin
from .models import Order, OrderItem
from catalog.models import CartItem 


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    list_display = [
                    'order_dish', 
                    'quantity' 
                   ]
    readonly_fields = (
                        'order_dish', 
                        'quantity'
                      )


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline,]
    list_display = [
                    'user',
                    'phone',
                    'total',
                    'deliverTo',
                    'address',
                    'personsAmount',
                    'orderStatus',
                    'created_at' 
                   ]


class OrderInline(admin.TabularInline):
    fk_name = 'user'
    model = Order
    readonly_fields = ('user', 'phone', 'total', 'deliverTo', 'address', 'personsAmount', 'paymentMode', 'created_at')
"""
class AddressInline(admin.TabularInline):
    fk_name = 'user'
    model = Address
    readonly_fields = ('user', 'street', 'building', 'porch', 'floor', 'apartment', 'comment', 'created_at')


class UserAdmin(admin.ModelAdmin):
    # form = UserAdminChangeForm 
    # add_form = UserAdminCreationForm

    # The fields to be use in displayin in the User model
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User
    inlines = [AddressInline, OrderInline]

    list_display = [  'phone', 'name','admin' ]
    list_filter = [ 'staff', 'active', 'admin',]
    fieldsets = (
        (None, {
            "fields": (
                'phone', 
            ),
        }),
        ('Personal info', {
            'fields': (
            'name',
        )}),
        # ('Permissions', {
        #     'fields': (
        #     'admin', 'staff', 'active'
        # )}),
    )

    search_fields = ('phone',)
    ordering = ('phone','name')
    list_filter = ('phone', 'name')
    filter_horizontal = ()  """

admin.site.register(Order, OrderAdmin)