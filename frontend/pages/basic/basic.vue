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
            <checkbox :value="item" :checked="basicInfo.limit_foods.includes(item)" color="#42b983" />
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
          <label class="checkbox-item" v-for="(item, index) in complicationsOptions" :key="index">
            <checkbox :value="item.value" :checked="basicInfo.complications.includes(item.value)" color="#42b983" />
            <text>{{ item.label }}</text>
          </label>
        </checkbox-group>
      </view>
      
      <view class="form-item complications-details" v-if="basicInfo.complications.length > 0">
        <text class="label">并发症确诊时间</text>
        <view class="complication-item" v-for="(item, index) in basicInfo.complications" :key="index">
          <text class="complication-name">{{ getComplicationLabel(item) }}</text>
          <picker 
            mode="date" 
            :value="basicInfo.complication_dates[item]" 
            @change="e => onComplicationDateChange(item, e.detail.value)"
            :end="today"
          >
            <view class="picker-value">
              <text>{{ basicInfo.complication_dates[item] || '请选择确诊时间' }}</text>
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
        
        <view class="medicine-item" v-for="(item, index) in basicInfo.medicines" :key="index">
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
                v-model="item.name"
              />
            </view>
            
            <view class="sub-item">
              <text class="sub-label">剂量</text>
              <input 
                class="input" 
                type="text" 
                placeholder="请输入剂量" 
                v-model="item.dosage"
              />
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
  limit_foods: [],
  complications: [],
  complication_dates: {},
  medicines: []
});

const attackFrequencyOptions = ['每月1次以下', '每月1-2次', '每月3次以上'];
const attackFrequencyIndex = ref(0);
const sodaFrequencyOptions = ['每天', '每周几次', '偶尔'];
const sodaFrequencyIndex = ref(0);
const goutTypeOptions = ['代谢障碍型', '生成过多型', '混合型'];
const limitFoodOptions = ['海鲜', '动物内脏', '啤酒', '红肉'];
const complicationsOptions = [
  { value: 'hypertension', label: '高血压' }, 
  { value: 'diabetes', label: '糖尿病' }, 
  { value: 'kidney_disease', label: '肾病' }, 
  { value: 'heart_disease', label: '心脏病' }]
;

const today = computed(() => {
  const date = new Date();
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
});

const loadBasicInfo = async () => {
  try {
    const token = uni.getStorageSync('token');
    if (!token) {
      uni.redirectTo({ url: '/pages/login/login' });
      return;
    }

    uni.showLoading({ title: '加载中...' });
    
    const res = await uni.request({
      url: `${API_BASE_URL}/condition/basic/`,
      method: 'GET',
      header: {
        'Authorization': `Bearer ${token}`
      }
    });

    uni.hideLoading();

    if (res.statusCode === 200 && res.data) {
      Object.assign(basicInfo, res.data);
      updatePickerIndexes();
    }
  } catch (error) {
    uni.hideLoading();
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    });
  }
};

const saveBasicInfo = async () => {
  try {
    const token = uni.getStorageSync('token');
    if (!token) {
      uni.redirectTo({ url: '/pages/login/login' });
      return;
    }

    uni.showLoading({ title: '保存中...' });

    const res = await uni.request({
      url: `${API_BASE_URL}/condition/basic/`,
      method: 'POST',
      header: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      data: basicInfo  // We can now send basicInfo directly
    });

    uni.hideLoading();

    if (res.statusCode === 200) {
      uni.showToast({
        title: '保存成功',
        icon: 'success'
      });
    } else {
      throw new Error('保存失败');
    }
  } catch (error) {
    uni.hideLoading();
    uni.showToast({
      title: '保存失败',
      icon: 'none'
    });
  }
};

const updatePickerIndexes = () => {
  const afIndex = attackFrequencyOptions.findIndex(item => item === basicInfo.attack_frequency);
  if (afIndex !== -1) attackFrequencyIndex.value = afIndex;
  
  const sfIndex = sodaFrequencyOptions.findIndex(item => item === basicInfo.soda_frequency);
  if (sfIndex !== -1) sodaFrequencyIndex.value = sfIndex;
};

const onAttackFrequencyChange = (e) => {
  const index = e.detail.value;
  basicInfo.attack_frequency = attackFrequencyOptions[index];
  attackFrequencyIndex.value = index;
};

const onSodaFrequencyChange = (e) => {
  const index = e.detail.value;
  basicInfo.soda_frequency = sodaFrequencyOptions[index];
  sodaFrequencyIndex.value = index;
};

const onLimitFoodChange = (e) => {
  basicInfo.limit_foods = e.detail.value;
};

const onComplicationsChange = (e) => {
  basicInfo.complications = e.detail.value;
};

const getComplicationLabel = (value) => {
  const option = complicationsOptions.find(opt => opt.value === value);
  return option ? option.label : value;
};

const addMedicine = () => {
  basicInfo.medicines.push({
    name: '',
    dosage: ''
  });
};

const deleteMedicine = (index) => {
  basicInfo.medicines.splice(index, 1);
};

const onComplicationDateChange = (complication, date) => {
  if (!basicInfo.complication_dates) {
    basicInfo.complication_dates = {};
  }
  basicInfo.complication_dates[complication] = date;
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
            width: 80rpx;
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
