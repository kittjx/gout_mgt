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
          :value="basicInfo.diagnosisDate" 
          @change="e => basicInfo.diagnosisDate = e.detail.value"
          :end="today"
        >
          <view class="picker-value">
            <text>{{ basicInfo.diagnosisDate || '请选择确诊时间' }}</text>
            <view class="arrow-right"></view>
          </view>
        </picker>
      </view>
      
      <view class="form-item">
        <text class="label">首次痛风发作时间</text>
        <picker 
          mode="date" 
          :value="basicInfo.firstAttackDate" 
          @change="e => basicInfo.firstAttackDate = e.detail.value"
          :end="today"
        >
          <view class="picker-value">
            <text>{{ basicInfo.firstAttackDate || '请选择首次发作时间' }}</text>
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
            <text>{{ basicInfo.attackFrequency || '请选择发作频率' }}</text>
            <view class="arrow-right"></view>
          </view>
        </picker>
      </view>
      
      <view class="form-item">
        <text class="label">既往发作程度 (0-10分，最痛10分，无痛0分)</text>
        <slider 
          :value="parseFloat(basicInfo.painLevel) || 0" 
          min="0" 
          max="10" 
          show-value 
          @change="e => basicInfo.painLevel = e.detail.value"
          activeColor="#42b983"
          block-color="#42b983"
        />
      </view>
      
      <view class="form-item">
        <text class="label">痛风分型</text>
        <radio-group @change="e => basicInfo.goutType = e.detail.value">
          <label class="radio-item" v-for="(item, index) in goutTypeOptions" :key="index">
            <radio :value="item" :checked="basicInfo.goutType === item" color="#42b983" />
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
        <radio-group @change="e => basicInfo.drinkingHistory = e.detail.value">
          <label class="radio-item">
            <radio value="无" :checked="basicInfo.drinkingHistory === '无'" color="#42b983" />
            <text>无</text>
          </label>
          <label class="radio-item">
            <radio value="偶尔" :checked="basicInfo.drinkingHistory === '偶尔'" color="#42b983" />
            <text>偶尔</text>
          </label>
          <label class="radio-item">
            <radio value="经常" :checked="basicInfo.drinkingHistory === '经常'" color="#42b983" />
            <text>经常</text>
          </label>
          <label class="radio-item">
            <radio value="已戒酒" :checked="basicInfo.drinkingHistory === '已戒酒'" color="#42b983" />
            <text>已戒酒</text>
          </label>
        </radio-group>
      </view>
      
      <view class="form-item">
        <text class="label">饮用碳酸饮料</text>
        <view class="sub-item">
          <text class="sub-label">是否饮用</text>
          <switch 
            :checked="basicInfo.drinkSoda" 
            @change="e => basicInfo.drinkSoda = e.detail.value"
            color="#42b983"
          />
        </view>
        
        <view class="sub-item" v-if="basicInfo.drinkSoda">
          <text class="sub-label">频率</text>
          <picker 
            :range="sodaFrequencyOptions" 
            :value="sodaFrequencyIndex" 
            @change="onSodaFrequencyChange"
          >
            <view class="picker-value">
              <text>{{ basicInfo.sodaFrequency || '请选择频率' }}</text>
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
            :checked="basicInfo.limitPurine" 
            @change="e => basicInfo.limitPurine = e.detail.value"
            color="#42b983"
          />
        </view>
        
        <view class="sub-item" v-if="basicInfo.limitPurine">
          <text class="sub-label">开始时间</text>
          <picker 
            mode="date" 
            :value="basicInfo.limitPurineDate" 
            @change="e => basicInfo.limitPurineDate = e.detail.value"
            :end="today"
          >
            <view class="picker-value">
              <text>{{ basicInfo.limitPurineDate || '请选择开始时间' }}</text>
              <view class="arrow-right"></view>
            </view>
          </picker>
        </view>
      </view>
      
      <view class="form-item" v-if="basicInfo.limitPurine">
        <text class="label">主要限制食物</text>
        <checkbox-group @change="onLimitFoodChange">
          <label class="checkbox-item" v-for="(item, index) in limitFoodOptions" :key="index">
            <checkbox :value="item" :checked="basicInfo.limitFoods.includes(item)" color="#42b983" />
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
            :value="basicInfo.complicationDates[item]" 
            @change="e => onComplicationDateChange(item, e.detail.value)"
            :end="today"
          >
            <view class="picker-value">
              <text>{{ basicInfo.complicationDates[item] || '请选择确诊时间' }}</text>
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
  </view>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';

// 获取当前日期
const today = new Date().toISOString().split('T')[0];

// 选项数据
const attackFrequencyOptions = ['每年1-2次', '每年3-5次', '每年6次以上', '每月至少1次'];
const sodaFrequencyOptions = ['每天', '每周数次', '每月数次', '很少'];
const limitFoodOptions = ['动物内脏', '肉汤', '海鲜', '零食'];
const goutTypeOptions = ['生成过多型', '排泄障碍型', '混合型'];
const complicationsOptions = [
  { value: 'hypertension', label: '高血压' },
  { value: 'diabetes', label: '糖尿病' },
  { value: 'hyperlipidemia', label: '高血脂' },
  { value: 'coronary', label: '冠心病' },
  { value: 'liver', label: '肝功能异常' },
  { value: 'kidney', label: '肾功能异常' }
];

// 索引值，用于选择器
const attackFrequencyIndex = ref(0);
const sodaFrequencyIndex = ref(0);

// 基础信息数据
const basicInfo = reactive({
  diagnosisDate: '',
  firstAttackDate: '',
  attackFrequency: '',
  painLevel: 0,
  drinkingHistory: '无',
  drinkSoda: false,
  sodaFrequency: '',
  limitPurine: false,
  limitPurineDate: '',
  limitFoods: [],
  goutType: '生成过多型',
  complications: [],
  complicationDates: {},
  medicines: []
});

// 处理发作频率选择
const onAttackFrequencyChange = (e) => {
  const index = e.detail.value;
  attackFrequencyIndex.value = index;
  basicInfo.attackFrequency = attackFrequencyOptions[index];
};

// 处理碳酸饮料频率选择
const onSodaFrequencyChange = (e) => {
  const index = e.detail.value;
  sodaFrequencyIndex.value = index;
  basicInfo.sodaFrequency = sodaFrequencyOptions[index];
};

// 处理限制食物选择
const onLimitFoodChange = (e) => {
  basicInfo.limitFoods = e.detail.value;
};

// 处理并发症选择
const onComplicationsChange = (e) => {
  basicInfo.complications = e.detail.value;
};

// 获取并发症标签
const getComplicationLabel = (value) => {
  const item = complicationsOptions.find(item => item.value === value);
  return item ? item.label : value;
};

// 处理并发症日期选择
const onComplicationDateChange = (complication, date) => {
  if (!basicInfo.complicationDates) {
    basicInfo.complicationDates = {};
  }
  basicInfo.complicationDates[complication] = date;
};

// 添加药物
const addMedicine = () => {
  basicInfo.medicines.push({
    name: '',
    dosage: ''
  });
};

// 删除药物
const deleteMedicine = (index) => {
  basicInfo.medicines.splice(index, 1);
};

// 保存基础信息
const saveBasicInfo = () => {
  // 基本验证
  if (!basicInfo.diagnosisDate) {
    uni.showToast({
      title: '请选择确诊时间',
      icon: 'none'
    });
    return;
  }
  
  // 保存数据到本地存储
  uni.setStorageSync('basicInfo', JSON.stringify(basicInfo));
  
  uni.showToast({
    title: '保存成功',
    icon: 'success'
  });
};

// 页面加载时获取本地存储的数据
onMounted(() => {
  const savedInfo = uni.getStorageSync('basicInfo');
  if (savedInfo) {
    try {
      const parsedInfo = JSON.parse(savedInfo);
      Object.assign(basicInfo, parsedInfo);
      
      // 更新选择器索引
      const afIndex = attackFrequencyOptions.findIndex(item => item === basicInfo.attackFrequency);
      if (afIndex !== -1) {
        attackFrequencyIndex.value = afIndex;
      }
      
      const sfIndex = sodaFrequencyOptions.findIndex(item => item === basicInfo.sodaFrequency);
      if (sfIndex !== -1) {
        sodaFrequencyIndex.value = sfIndex;
      }
    } catch (e) {
      console.error('解析基础信息失败', e);
    }
  }
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
