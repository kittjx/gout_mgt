from django.contrib import admin
from .models import BasicCondition, LimitFood, Complication, Medicine

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
