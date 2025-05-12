from django.contrib import admin
from .models import (
    Record, WeightRecord, MainFoodRecord, WaterIntakeRecord, 
    PurineFoodRecord, UricAcidRecord, UrinePHRecord, LiverFunctionRecord,
    KidneyFunctionRecord, BloodSugarRecord, BloodPressureRecord, BloodLipidRecord,
    AttackRecord, TophiRecord, SurgeryRecord, JointFunctionRecord,
    UserRecordsView
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

class UserRecordsViewAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'user_phone', 'record_type', 'date', 'get_record_value')
    list_filter = ('record_type', 'user_phone', 'date')
    search_fields = ('user_phone', 'record_type')
    date_hierarchy = 'date'
    readonly_fields = [field.name for field in UserRecordsView._meta.get_fields()]
    
    def get_record_value(self, obj):
        """Return the appropriate value based on record type"""
        if obj.record_type == 'weight':
            return f"{obj.weight_value} kg"
        elif obj.record_type == 'mainFood':
            return f"{obj.main_food_name}: {obj.main_food_amount}"
        elif obj.record_type == 'waterIntake':
            return f"{obj.water_intake_amount}"
        elif obj.record_type == 'purineFood':
            return f"{obj.purine_food_type}: {obj.purine_food_amount}"
        elif obj.record_type == 'uricAcid':
            return f"{obj.uric_acid_value} ({obj.uric_acid_method})"
        elif obj.record_type == 'urinePH':
            return f"{obj.urine_ph_value}"
        elif obj.record_type == 'liverFunction':
            return f"{obj.liver_function_value}"
        elif obj.record_type == 'kidneyFunction':
            return f"{obj.kidney_function_value}"
        elif obj.record_type == 'bloodSugar':
            return f"{obj.blood_sugar_value}"
        elif obj.record_type == 'bloodPressure':
            return f"{obj.blood_pressure_value}"
        elif obj.record_type == 'bloodLipid':
            return f"{obj.blood_lipid_value}"
        elif obj.record_type == 'attack':
            return f"疼痛: {obj.attack_pain_score}, 持续: {obj.attack_duration}天"
        elif obj.record_type == 'tophi':
            return f"{obj.tophi_location}: {obj.tophi_size}"
        elif obj.record_type == 'surgery':
            return f"{obj.surgery_location}"
        elif obj.record_type == 'jointFunction':
            return f"{obj.joint_function_joint}: {obj.joint_function_description}"
        return "未知"
    
    get_record_value.short_description = '记录值'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

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
admin.site.register(UserRecordsView, UserRecordsViewAdmin)
