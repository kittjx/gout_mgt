from rest_framework import serializers
from .models import BasicCondition, LimitFood, Complication, Medicine, PatientConditionView

class LimitFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitFood
        fields = ['id', 'name']

class ComplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complication
        fields = ['id', 'name', 'diagnosis_date']

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'dosage', 'start_date']

class BasicConditionSerializer(serializers.ModelSerializer):
    limit_foods = LimitFoodSerializer(many=True, read_only=True)
    complications = ComplicationSerializer(many=True, read_only=True)
    medicines = MedicineSerializer(many=True, read_only=True)
    
    # These fields are used for write operations
    limit_food_names = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True,
        required=False
    )
    
    complication_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    medicine_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = BasicCondition
        fields = [
            'id', 'diagnosis_date', 'first_attack_date', 'attack_frequency',
            'pain_level', 'gout_type', 'drinking_history', 'drink_soda',
            'soda_frequency', 'limit_purine', 'limit_purine_date',
            'limit_foods', 'complications', 'medicines',
            'limit_food_names', 'complication_data', 'medicine_data',
            'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        limit_food_names = validated_data.pop('limit_food_names', [])
        complication_data = validated_data.pop('complication_data', [])
        medicine_data = validated_data.pop('medicine_data', [])
        
        basic_condition = BasicCondition.objects.create(**validated_data)
        
        # Create limit foods
        for name in limit_food_names:
            LimitFood.objects.create(basic_condition=basic_condition, name=name)
        
        # Create complications
        for comp_data in complication_data:
            Complication.objects.create(
                basic_condition=basic_condition,
                name=comp_data.get('name', ''),
                diagnosis_date=comp_data.get('diagnosis_date')
            )
        
        # Create medicines
        for med_data in medicine_data:
            Medicine.objects.create(
                basic_condition=basic_condition,
                name=med_data.get('name', ''),
                dosage=med_data.get('dosage', ''),
                start_date=med_data.get('start_date')
            )
        
        return basic_condition
    
    def update(self, instance, validated_data):
        limit_food_names = validated_data.pop('limit_food_names', None)
        complication_data = validated_data.pop('complication_data', None)
        medicine_data = validated_data.pop('medicine_data', None)
        
        # Update basic condition fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update limit foods if provided
        if limit_food_names is not None:
            # Delete existing limit foods
            instance.limit_foods.all().delete()
            
            # Create new limit foods
            for name in limit_food_names:
                LimitFood.objects.create(basic_condition=instance, name=name)
        
        # Update complications if provided
        if complication_data is not None:
            # Delete existing complications
            instance.complications.all().delete()
            
            # Create new complications
            for comp_data in complication_data:
                Complication.objects.create(
                    basic_condition=instance,
                    name=comp_data.get('name', ''),
                    diagnosis_date=comp_data.get('diagnosis_date')
                )
        
        # Update medicines if provided
        if medicine_data is not None:
            # Delete existing medicines
            instance.medicines.all().delete()
            
            # Create new medicines
            for med_data in medicine_data:
                Medicine.objects.create(
                    basic_condition=instance,
                    name=med_data.get('name', ''),
                    dosage=med_data.get('dosage', ''),
                    start_date=med_data.get('start_date')
                )
        
        return instance

class PatientConditionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientConditionView
        fields = '__all__'
