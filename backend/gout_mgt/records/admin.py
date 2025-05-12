from django.contrib import admin
from .models import (
    Record, WeightRecord, MainFoodRecord, WaterIntakeRecord, 
    PurineFoodRecord, UricAcidRecord, UrinePHRecord, LiverFunctionRecord,
    KidneyFunctionRecord, BloodSugarRecord, BloodPressureRecord, BloodLipidRecord,
    AttackRecord, TophiRecord, SurgeryRecord, JointFunctionRecord
)

class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'record_type', 'date', 'created_at')
    list_filter = ('record_type', 'created_at')
    search_fields = ('user__phone', 'record_type')
    date_hierarchy = 'date'

class WeightRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'value')
    search_fields = ('record__user__phone',)

class MainFoodRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'name', 'amount')
    search_fields = ('record__user__phone', 'name')

class WaterIntakeRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'amount')
    search_fields = ('record__user__phone',)

class PurineFoodRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'type', 'amount')
    search_fields = ('record__user__phone', 'type')

class UricAcidRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'value', 'method')
    search_fields = ('record__user__phone',)

class UrinePHRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'value')
    search_fields = ('record__user__phone',)

class LiverFunctionRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'value')
    search_fields = ('record__user__phone',)

class KidneyFunctionRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'value')
    search_fields = ('record__user__phone',)

class BloodSugarRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'value')
    search_fields = ('record__user__phone',)

class BloodPressureRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'value')
    search_fields = ('record__user__phone',)

class BloodLipidRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'value')
    search_fields = ('record__user__phone',)

class AttackRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'pain_score', 'duration')
    search_fields = ('record__user__phone',)

class TophiRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'location', 'size')
    search_fields = ('record__user__phone', 'location')

class SurgeryRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'location', 'notes')
    search_fields = ('record__user__phone', 'location')

class JointFunctionRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'joint', 'description')
    search_fields = ('record__user__phone', 'joint')

# Register all models
admin.site.register(Record, RecordAdmin)
admin.site.register(WeightRecord, WeightRecordAdmin)
admin.site.register(MainFoodRecord, MainFoodRecordAdmin)
admin.site.register(WaterIntakeRecord, WaterIntakeRecordAdmin)
admin.site.register(PurineFoodRecord, PurineFoodRecordAdmin)
admin.site.register(UricAcidRecord, UricAcidRecordAdmin)
admin.site.register(UrinePHRecord, UrinePHRecordAdmin)
admin.site.register(LiverFunctionRecord, LiverFunctionRecordAdmin)
admin.site.register(KidneyFunctionRecord, KidneyFunctionRecordAdmin)
admin.site.register(BloodSugarRecord, BloodSugarRecordAdmin)
admin.site.register(BloodPressureRecord, BloodPressureRecordAdmin)
admin.site.register(BloodLipidRecord, BloodLipidRecordAdmin)
admin.site.register(AttackRecord, AttackRecordAdmin)
admin.site.register(TophiRecord, TophiRecordAdmin)
admin.site.register(SurgeryRecord, SurgeryRecordAdmin)
admin.site.register(JointFunctionRecord, JointFunctionRecordAdmin)
