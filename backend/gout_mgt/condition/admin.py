from django.contrib import admin
from .models import BasicCondition, LimitFood, Complication, Medicine, PatientConditionView

class LimitFoodInline(admin.TabularInline):
    model = LimitFood
    extra = 1

class ComplicationInline(admin.TabularInline):
    model = Complication
    extra = 1

class MedicineInline(admin.TabularInline):
    model = Medicine
    extra = 1

class BasicConditionAdmin(admin.ModelAdmin):
    list_display = ('user', 'diagnosis_date', 'gout_type', 'created_at')
    search_fields = ('user__phone', 'gout_type')
    inlines = [LimitFoodInline, ComplicationInline, MedicineInline]

admin.site.register(BasicCondition, BasicConditionAdmin)
admin.site.register(LimitFood)
admin.site.register(Complication)
admin.site.register(Medicine)

class PatientConditionViewAdmin(admin.ModelAdmin):
    list_display = ('condition_id', 'user_phone', 'gout_type', 'diagnosis_date', 'get_limit_foods_count', 'get_complications_count', 'get_medicines_count')
    list_filter = ('gout_type', 'drink_soda', 'limit_purine')
    search_fields = ('user_phone', 'gout_type')
    readonly_fields = [field.name for field in PatientConditionView._meta.get_fields()]
    
    def get_limit_foods_count(self, obj):
        """Return the count of limit foods"""
        return len(obj.limit_foods)
    
    def get_complications_count(self, obj):
        """Return the count of complications"""
        return len(obj.complications)
    
    def get_medicines_count(self, obj):
        """Return the count of medicines"""
        return len(obj.medicines)
    
    get_limit_foods_count.short_description = '限制食物数量'
    get_complications_count.short_description = '并发症数量'
    get_medicines_count.short_description = '药物数量'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(PatientConditionView, PatientConditionViewAdmin)
