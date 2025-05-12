<template>
  <view class="basic-info-container">
    <view class="page-header">
      <text class="tips">请完善您的痛风相关基础病情信息</text>
    </view>
    
    <view class="info-section">
      <view class="section-title">
        <view class="title-bar"></view>
        <text>疾病信息</text>
      </view>
      
      <view class="form-item">
        <text class="label">高尿酸血症确诊时间</text>
        <picker 
          mode="date" 
          :value="basicInfo.diagnosis_date" 
          @change="e => basicInfo.diagnosis_date = e.detail.value"
          :end="today"
        >
          <view class="picker-value">
            <text>{{ basicInfo.diagnosis_date || '请选择确诊时间' }}</text>
            <view class="arrow-right"></view>
          </view>
        </picker>
      </view>
      
      <view class="form-item">
        <text class="label">首次痛风发作时间</text>
        <picker 
          mode="date" 
          :value="basicInfo.first_attack_date" 
          @change="e => basicInfo.first_attack_date = e.detail.value"
          :end="today"
        >
          <view class="picker-value">
            <text>{{ basicInfo.first_attack_date || '请选择首次发作时间' }}</text>
            <view class="arrow-right"></view>
          </view>
        </picker>
      </view>
      
      <view class="form-item">
        <text class="label">既往发作频率</text>
        <picker 
          :range="attackFrequencyOptions" 
          :value="attackFrequencyIndex" 
          @change="onAttackFrequencyChange"
        >
          <view class="picker-value">
            <text>{{ basicInfo.attack_frequency || '请选择发作频率' }}</text>
            <view class="arrow-right"></view>
          </view>
        </picker>
      </view>
      
      <view class="form-item">
        <text class="label">既往发作程度 (0-10分，最痛10分，无痛0分)</text>
        <slider 
          :value="parseFloat(basicInfo.pain_level) || 0" 
          min="0" 
          max="10" 
          show-value 
          @change="e => basicInfo.pain_level = e.detail.value"
          activeColor="#42b983"
          block-color="#42b983"
        />
      </view>
      
      <view class="form-item">
        <text class="label">痛风分型</text>
        <radio-group @change="e => basicInfo.gout_type = e.detail.value">
          <label class="radio-item" v-for="(item, index) in goutTypeOptions" :key="index">
            <radio :value="item" :checked="basicInfo.gout_type === item" color="#42b983" />
            <text>{{ item }}</text>
          </label>
        </radio-group>
      </view>
    </view>
    
    <view class="info-section">
      <view class="section-title">
        <view class="title-bar"></view>
        <text>生活习惯</text>
      </view>
      
      <view class="form-item">
        <text class="label">饮酒史</text>
        <radio-group @change="e => basicInfo.drinking_history = e.detail.value">
          <label class="radio-item">
            <radio value="无" :checked="basicInfo.drinking_history === '无'" color="#42b983" />
            <text>无</text>
          </label>
          <label class="radio-item">
            <radio value="偶尔" :checked="basicInfo.drinking_history === '偶尔'" color="#42b983" />
            <text>偶尔</text>
          </label>
          <label class="radio-item">
            <radio value="经常" :checked="basicInfo.drinking_history === '经常'" color="#42b983" />
            <text>经常</text>
          </label>
          <label class="radio-item">
            <radio value="已戒酒" :checked="basicInfo.drinking_history === '已戒酒'" color="#42b983" />
            <text>已戒酒</text>
          </label>
        </radio-group>
      </view>
      
      <view class="form-item">
        <text class="label">饮用碳酸饮料</text>
        <view class="sub-item">
          <text class="sub-label">是否饮用</text>
          <switch 
            :checked="basicInfo.drink_soda" 
            @change="e => basicInfo.drink_soda = e.detail.value"
            color="#42b983"
          />
        </view>
        
        <view class="sub-item" v-if="basicInfo.drink_soda">
          <text class="sub-label">频率</text>
          <picker 
            :range="sodaFrequencyOptions" 
            :value="sodaFrequencyIndex" 
            @change="onSodaFrequencyChange"
          >
            <view class="picker-value">
              <text>{{ basicInfo.soda_frequency || '请选择频率' }}</text>
              <view class="arrow-right"></view>
            </view>
          </picker>
        </view>
      </view>
      
      <view class="form-item">
        <text class="label">限制高嘌呤食物</text>
        <view class="sub-item">
          <text class="sub-label">是否限制</text>
          <switch 
            :checked="basicInfo.limit_purine" 
            @change="e => basicInfo.limit_purine = e.detail.value"
            color="#42b983"
          />
        </view>
        
        <view class="sub-item" v-if="basicInfo.limit_purine">
          <text class="sub-label">开始时间</text>
          <picker 
            mode="date" 
            :value="basicInfo.limit_purine_date" 
            @change="e => basicInfo.limit_purine_date = e.detail.value"
            :end="today"
          >
            <view class="picker-value">
              <text>{{ basicInfo.limit_purine_date || '请选择开始时间' }}</text>
              <view class="arrow-right"></view>
            </view>
          </picker>
        </view>
      </view>
      
      <view class="form-item" v-if="basicInfo.limit_purine">
        <text class="label">主要限制食物</text>
        <checkbox-group @change="onLimitFoodChange">
          <label class="checkbox-item" v-for="(item, index) in limitFoodOptions" :key="index">
            <checkbox :value="item" :checked="limitFoods.includes(item)" color="#42b983" />
            <text>{{ item }}</text>
          </label>
        </checkbox-group>
      </view>
    </view>
    
    <view class="info-section">
      <view class="section-title">
        <view class="title-bar"></view>
        <text>并发症与用药情况</text>
      </view>
      
      <view class="form-item">
        <text class="label">是否有并发症</text>
        <checkbox-group @change="onComplicationsChange">
          <label class="checkbox-item" v-for="(item, index) in complicationOptions" :key="index">
            <checkbox :value="item.value" :checked="hasComplication(item.value)" color="#42b983" />
            <text>{{ item.label }}</text>
          </label>
        </checkbox-group>
      </view>
      
      <view class="form-item complications-details" v-if="complications.length > 0">
        <text class="label">并发症确诊时间</text>
        <view class="complication-item" v-for="comp in complications" :key="comp.id">
          <text class="complication-name">{{ getComplicationLabel(comp.name) }}</text>
          <picker 
            mode="date" 
            :value="comp.diagnosis_date" 
            @change="e => onComplicationDateChange(comp.id, e.detail.value)"
            :end="today"
          >
            <view class="picker-value">
              <text>{{ comp.diagnosis_date || '请选择确诊时间' }}</text>
              <view class="arrow-right"></view>
            </view>
          </picker>
        </view>
      </view>
      
      <view class="form-item">
        <text class="label">服用药物</text>
        <view class="add-medicine" @tap="addMedicine">
          <text class="plus-icon">+</text>
          <text>添加药物</text>
        </view>
        
        <view class="medicine-item" v-for="(med, index) in medicines" :key="med.id || index">
          <view class="medicine-header">
            <text class="medicine-title">药物 {{ index + 1 }}</text>
            <text class="delete-btn" @tap="deleteMedicine(index)">删除</text>
          </view>
          
          <view class="medicine-form">
            <view class="sub-item">
              <text class="sub-label">药名</text>
              <input 
                class="input" 
                type="text" 
                placeholder="请输入药名" 
                v-model="med.name"
              />
            </view>
            
            <view class="sub-item">
              <text class="sub-label">剂量</text>
              <input 
                class="input" 
                type="text" 
                placeholder="请输入剂量" 
                v-model="med.dosage"
              />
            </view>
            
            <view class="sub-item">
              <text class="sub-label">开始时间</text>
              <picker 
                mode="date" 
                :value="med.start_date" 
                @change="e => onMedicineStartDateChange(med.id || index, e.detail.value)"
                :end="today"
              >
                <view class="picker-value">
                  <text>{{ med.start_date || '请选择开始时间' }}</text>
                  <view class="arrow-right"></view>
                </view>
              </picker>
            </view>
          </view>
        </view>
      </view>
    </view>
    
    <button class="save-btn" @tap="saveBasicInfo">保存信息</button>
    <LogoutButton />
  </view>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { API_BASE_URL } from '@/utils/config.js';
import LogoutButton from '@/components/LogoutButton.vue';

// Complication options
const complicationOptions = [
  { label: '高血压', value: 'hypertension' },
  { label: '糖尿病', value: 'diabetes' },
  { label: '肾病', value: 'kidney_disease' },
  { label: '心脏病', value: 'heart_disease' }
];

// Basic info data
const basicInfo = reactive({
  diagnosis_date: '',
  first_attack_date: '',
  attack_frequency: '',
  pain_level: 0,
  gout_type: '',
  drinking_history: '',
  drink_soda: false,
  soda_frequency: '',
  limit_purine: false,
  limit_purine_date: '',
});

// Separate reactive arrays for related data
const complications = ref([]);
const medicines = ref([]);
const limitFoods = ref([]);

const attackFrequencyOptions = ['每月1次以下', '每月1-2次', '每月3次以上'];
const attackFrequencyIndex = ref(0);
const sodaFrequencyOptions = ['每天', '每周几次', '偶尔'];
const sodaFrequencyIndex = ref(0);
const goutTypeOptions = ['代谢障碍型', '生成过多型', '混合型'];
const limitFoodOptions = ['海鲜', '动物内脏', '啤酒', '红肉'];

const today = computed(() => {
  const date = new Date();
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
});

// Check if a complication exists
const hasComplication = (value) => {
  return complications.value.some(comp => comp.name === value);
};

// Get the label for a complication value
const getComplicationLabel = (value) => {
  const option = complicationOptions.find(opt => opt.value === value);
  return option ? option.label : value;
};

// Handle complications change
const onComplicationsChange = (e) => {
  const selectedValues = e.detail.value;
  
  // Remove complications that are no longer selected
  complications.value = complications.value.filter(comp => 
    selectedValues.includes(comp.name)
  );
  
  // Add newly selected complications
  selectedValues.forEach(value => {
    if (!hasComplication(value)) {
      complications.value.push({
        id: Date.now() + Math.random(), // Temporary ID for frontend
        name: value,
        diagnosis_date: ''
      });
    }
  });
};

// Handle complication date change
const onComplicationDateChange = (compId, date) => {
  const comp = complications.value.find(c => c.id === compId);
  if (comp) {
    comp.diagnosis_date = date;
  }
};

// Handle medicine start date change
const onMedicineStartDateChange = (medicineId, date) => {
  const med = medicines.value.find((m, idx) => m.id === medicineId || idx === medicineId);
  if (med) {
    med.start_date = date;
  }
};

// Add a new medicine
const addMedicine = () => {
  medicines.value.push({
    id: Date.now() + Math.random(), // Temporary ID for frontend
    name: '',
    dosage: '',
    start_date: ''
  });
};

// Delete a medicine
const deleteMedicine = (index) => {
  if (index >= 0 && index < medicines.value.length) {
    medicines.value.splice(index, 1);
  }
};

// Handle limit food change
const onLimitFoodChange = (e) => {
  limitFoods.value = e.detail.value;
};

// Handle attack frequency change
const onAttackFrequencyChange = (e) => {
  const index = e.detail.value;
  basicInfo.attack_frequency = attackFrequencyOptions[index];
  attackFrequencyIndex.value = index;
};

// Handle soda frequency change
const onSodaFrequencyChange = (e) => {
  const index = e.detail.value;
  basicInfo.soda_frequency = sodaFrequencyOptions[index];
  sodaFrequencyIndex.value = index;
};

// Update picker indexes based on current values
const updatePickerIndexes = () => {
  const afIndex = attackFrequencyOptions.findIndex(item => item === basicInfo.attack_frequency);
  if (afIndex !== -1) attackFrequencyIndex.value = afIndex;
  
  const sfIndex = sodaFrequencyOptions.findIndex(item => item === basicInfo.soda_frequency);
  if (sfIndex !== -1) sodaFrequencyIndex.value = sfIndex;
};

// Load basic info from API
const loadBasicInfo = async () => {
  try {
    const token = uni.getStorageSync('token');
    if (!token) {
      uni.redirectTo({ url: '/pages/login/login' });
      return;
    }

    uni.showLoading({ title: '加载中...' });
    
    const res = await uni.request({
      url: `${API_BASE_URL}/condition/`,
      method: 'GET',
      header: {
        'Authorization': `Bearer ${token}`
      }
    });

    uni.hideLoading();

    if (res.statusCode === 200 && res.data) {
      // Update basic info
      Object.keys(basicInfo).forEach(key => {
        if (res.data[key] !== undefined) {
          basicInfo[key] = res.data[key];
        }
      });
      
      // Update complications
      if (res.data.complications && Array.isArray(res.data.complications)) {
        complications.value = res.data.complications.map(comp => ({
          id: comp.id || Date.now() + Math.random(),
          name: comp.name,
          diagnosis_date: comp.diagnosis_date || ''
        }));
      }
      
      // Update medicines
      if (res.data.medicines && Array.isArray(res.data.medicines)) {
        medicines.value = res.data.medicines.map(med => ({
          id: med.id || Date.now() + Math.random(),
          name: med.name || '',
          dosage: med.dosage || '',
          start_date: med.start_date || ''
        }));
      }
      
      // Update limit foods
      if (res.data.limit_foods && Array.isArray(res.data.limit_foods)) {
        limitFoods.value = res.data.limit_foods.map(item => item.name);
      }
      
      // Update picker indexes
      updatePickerIndexes();
    }
  } catch (error) {
    uni.hideLoading();
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    });
    console.error('加载基础信息错误:', error);
  }
};

// Save basic info to API
const saveBasicInfo = async () => {
  try {
    const token = uni.getStorageSync('token');
    if (!token) {
      uni.redirectTo({ url: '/pages/login/login' });
      return;
    }

    // Validate data
    if (basicInfo.limit_purine && !basicInfo.limit_purine_date) {
      uni.showToast({
        title: '请选择限制高嘌呤食物的开始时间',
        icon: 'none'
      });
      return;
    }

    // Validate complications have dates
    const missingDates = complications.value.filter(comp => !comp.diagnosis_date);
    if (missingDates.length > 0) {
      uni.showToast({
        title: '请为所有并发症选择确诊时间',
        icon: 'none'
      });
      return;
    }

    // Validate medicines
    const incompleteMedicines = medicines.value.filter(med => !med.name || !med.dosage);
    if (incompleteMedicines.length > 0) {
      uni.showToast({
        title: '请完善所有药物的信息',
        icon: 'none'
      });
      return;
    }

    uni.showLoading({ title: '保存中...' });

    // Prepare data for API
    const dataToSend = {
      ...basicInfo,
      complication_data: complications.value.map(comp => ({
        name: comp.name,
        diagnosis_date: comp.diagnosis_date
      })),
      medicine_data: medicines.value.map(med => ({
        name: med.name,
        dosage: med.dosage,
        start_date: med.start_date || ''
      })),
      limit_food_names: limitFoods.value
    };

    const res = await uni.request({
      url: `${API_BASE_URL}/condition/`,
      method: 'POST',
      header: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      data: dataToSend
    });

        uni.hideLoading();

    if (res.statusCode === 200) {
      uni.showToast({
        title: '保存成功',
        icon: 'success'
      });

      // Update local data with response data
      if (res.data) {
        // Update basic info
        Object.keys(basicInfo).forEach(key => {
          if (res.data[key] !== undefined) {
            basicInfo[key] = res.data[key];
          }
        });
        
        // Update complications
        if (res.data.complications && Array.isArray(res.data.complications)) {
          complications.value = res.data.complications.map(comp => ({
            id: comp.id || Date.now() + Math.random(),
            name: comp.name,
            diagnosis_date: comp.diagnosis_date || ''
          }));
        }
        
        // Update medicines
        if (res.data.medicines && Array.isArray(res.data.medicines)) {
          medicines.value = res.data.medicines.map(med => ({
            id: med.id || Date.now() + Math.random(),
            name: med.name || '',
            dosage: med.dosage || '',
            start_date: med.start_date || ''
          }));
        }
        
        // Update limit foods
        if (res.data.limit_foods && Array.isArray(res.data.limit_foods)) {
          limitFoods.value = res.data.limit_foods.map(item => item.name);
        }
      }
    } else {
      throw new Error((res.data && res.data.error) || '保存失败');
    }
  } catch (error) {
    uni.hideLoading();
    uni.showToast({
      title: error.message || '保存失败',
      icon: 'none'
    });
    console.error('保存基础信息错误:', error);
  }
};

onMounted(() => {
  loadBasicInfo();
});
</script>

<style lang="scss">
.basic-info-container {
  min-height: 100vh;
  padding: 30rpx;
  box-sizing: border-box;
  background-color: #f8f8f8;
  padding-bottom: 120rpx;
}

.page-header {
  margin-bottom: 30rpx;
  
  .page-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 10rpx;
    display: block;
  }
  
  .tips {
    font-size: 26rpx;
    color: #888;
  }
}

.info-section {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
  margin-bottom: 30rpx;
  
  .section-title {
    display: flex;
    align-items: center;
    margin-bottom: 30rpx;
    
    .title-bar {
      width: 6rpx;
      height: 32rpx;
      background-color: #42b983;
      margin-right: 16rpx;
      border-radius: 3rpx;
    }
    
    text {
      font-size: 32rpx;
      font-weight: bold;
      color: #333;
    }
  }
  
  .form-item {
    position: relative;
    margin-bottom: 30rpx;
    
    .label {
      display: block;
      font-size: 28rpx;
      color: #666;
      margin-bottom: 12rpx;
    }
    
    .input {
      width: 100%;
      height: 80rpx;
      background-color: #f5f7fa;
      border-radius: 8rpx;
      padding: 0 20rpx;
      font-size: 28rpx;
      color: #333;
      box-sizing: border-box;
    }
    
    .picker-value {
      width: 100%;
      height: 80rpx;
      background-color: #f5f7fa;
      border-radius: 8rpx;
      padding: 0 20rpx;
      font-size: 28rpx;
      color: #333;
      box-sizing: border-box;
      display: flex;
      align-items: center;
      justify-content: space-between;
      
      .arrow-right {
        width: 16rpx;
        height: 16rpx;
        border-top: 2rpx solid #999;
        border-right: 2rpx solid #999;
        transform: rotate(45deg);
      }
    }
    
    .radio-item, .checkbox-item {
      display: flex;
      align-items: center;
      margin-bottom: 20rpx;
      font-size: 28rpx;
      color: #333;
    }
    
    .sub-item {
      display: flex;
      align-items: center;
      margin-bottom: 20rpx;
      
      .sub-label {
        font-size: 26rpx;
        color: #666;
        width: 120rpx;
      }
    }
    
    &.complications-details {
      .complication-item {
        display: flex;
        align-items: center;
        margin-bottom: 20rpx;
        
        .complication-name {
          font-size: 26rpx;
          color: #666;
          width: 140rpx;
        }
        
        .picker-value {
          flex: 1;
        }
      }
    }
    
    .add-medicine {
      display: flex;
      align-items: center;
      margin-bottom: 20rpx;
      font-size: 28rpx;
      color: #42b983;
      
      .plus-icon {
        margin-right: 10rpx;
        font-size: 32rpx;
        font-weight: bold;
      }
    }
    
    .medicine-item {
      background-color: #f5f7fa;
      border-radius: 8rpx;
      padding: 20rpx;
      margin-bottom: 20rpx;
      
      .medicine-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20rpx;
        
        .medicine-title {
          font-size: 28rpx;
          font-weight: bold;
          color: #333;
        }
        
        .delete-btn {
          font-size: 26rpx;
          color: #ff4949;
        }
      }
      
      .medicine-form {
        .sub-item {
          display: flex;
          align-items: center;
          margin-bottom: 20rpx;
          
          .sub-label {
            font-size: 26rpx;
            color: #666;
            width: 120rpx;
            white-space: nowrap;
          }
          
          .input {
            flex: 1;
            height: 70rpx;
          }
        }
      }
    }
  }
}

.save-btn {
  width: 100%;
  height: 90rpx;
  background-color: #42b983;
  color: #fff;
  border-radius: 45rpx;
  font-size: 32rpx;
  font-weight: bold;
  line-height: 90rpx;
  margin-top: 20rpx;
  margin-bottom: 30rpx;
}
</style>