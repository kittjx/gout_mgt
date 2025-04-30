<template>
  <view class="personal-info-container">
    <view class="page-header">
      <text class="tips">请完善您的个人基本信息</text>
    </view>
    
    <view class="info-form">
      <view class="form-item">
        <text class="label">姓名</text>
        <input 
          class="input" 
          type="text" 
          placeholder="请输入您的真实姓名" 
          v-model="personalInfo.name"
        />
      </view>
      
      <view class="form-item">
        <text class="label">手机号码</text>
        <input 
          class="input" 
          type="number" 
          placeholder="请输入手机号" 
          maxlength="11"
          v-model="personalInfo.phone"
        />
      </view>
      
      <view class="form-item">
        <text class="label">性别</text>
        <view class="gender-selector">
          <view 
            class="gender-option" 
            :class="{ active: personalInfo.gender === '男' }"
            @tap="personalInfo.gender = '男'"
          >
            <text>男</text>
          </view>
          <view 
            class="gender-option" 
            :class="{ active: personalInfo.gender === '女' }"
            @tap="personalInfo.gender = '女'"
          >
            <text>女</text>
          </view>
        </view>
      </view>
      
      <view class="form-item">
        <text class="label">出生日期</text>
        <picker 
          mode="date" 
          :value="personalInfo.birthday" 
          @change="onBirthdayChange"
          :end="today"
        >
          <view class="picker-value">
            <text>{{ personalInfo.birthday || '请选择出生日期' }}</text>
            <view class="arrow-right"></view>
          </view>
        </picker>
      </view>
      
      <view class="form-item">
        <text class="label">身高 (cm)</text>
        <input 
          class="input" 
          type="digit" 
          placeholder="请输入身高" 
          v-model="personalInfo.height"
          @input="calculateBMI"
        />
      </view>
      
      <view class="form-item">
        <text class="label">体重 (kg)</text>
        <input 
          class="input" 
          type="digit" 
          placeholder="请输入体重" 
          v-model="personalInfo.weight"
          @input="calculateBMI"
        />
      </view>
      
      <view class="form-item">
        <text class="label">BMI</text>
        <view class="bmi-value">
          <text>{{ bmiValue }}</text>
          <text class="bmi-status" :class="bmiStatusClass">{{ bmiStatus }}</text>
        </view>
      </view>
      
      
    </view>
    
    <button class="save-btn" @tap="savePersonalInfo">保存信息</button>
    <LogoutButton />
  </view>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue';
import LogoutButton from '@/components/LogoutButton.vue';
import { API_BASE_URL } from '@/utils/config.js';

// 获取当前日期
const today = new Date().toISOString().split('T')[0];

// 个人信息数据
const personalInfo = reactive({
  name: '',
  gender: '男',
  birthday: '',
  height: '',
  weight: '',
  phone: '',
  emergencyContact: '',
  emergencyPhone: ''
});

// BMI值计算
const bmiValue = computed(() => {
  if (!personalInfo.height || !personalInfo.weight) return '未计算';
  
  const height = parseFloat(personalInfo.height) / 100; // 转换为米
  const weight = parseFloat(personalInfo.weight);
  
  if (!height || !weight) return '未计算';
  
  const bmi = weight / (height * height);
  return bmi.toFixed(1);
});

// BMI状态判断
const bmiStatus = computed(() => {
  const bmi = parseFloat(bmiValue.value);
  if (bmi === NaN || bmiValue.value === '未计算') return '';
  
  if (bmi < 18.5) return '偏瘦';
  if (bmi >= 18.5 && bmi < 24) return '正常';
  if (bmi >= 24 && bmi < 28) return '超重';
  if (bmi >= 28) return '肥胖';
  
  return '';
});

// BMI状态对应的样式类
const bmiStatusClass = computed(() => {
  switch (bmiStatus.value) {
    case '偏瘦': return 'underweight';
    case '正常': return 'normal';
    case '超重': return 'overweight';
    case '肥胖': return 'obese';
    default: return '';
  }
});

// 计算BMI
const calculateBMI = () => {
  // BMI已通过计算属性自动计算
};

// 出生日期变更
const onBirthdayChange = (e) => {
  personalInfo.birthday = e.detail.value;
};

// 保存个人信息
const savePersonalInfo = async () => {
  // 表单验证
  if (!personalInfo.name) {
    uni.showToast({
      title: '请输入姓名',
      icon: 'none'
    });
    return;
  }
  
  if (!personalInfo.birthday) {
    uni.showToast({
      title: '请选择出生日期',
      icon: 'none'
    });
    return;
  }
  
  if (!personalInfo.height) {
    uni.showToast({
      title: '请输入身高',
      icon: 'none'
    });
    return;
  }
  
  if (!personalInfo.weight) {
    uni.showToast({
      title: '请输入体重',
      icon: 'none'
    });
    return;
  }
  
  try {
    // Show loading
    uni.showLoading({
      title: '保存中...'
    });
    
    // Get token from storage
    const token = uni.getStorageSync('token');
    if (!token) {
      throw new Error('登录已过期，请重新登录');
    }
    
    // Send data to backend
    const res = await uni.request({
      url: `${API_BASE_URL}/patient/profile/`,
      method: 'POST',
      data: personalInfo,
      header: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      dataType: 'json',
      withCredentials: true
    });
    
    // Hide loading
    uni.hideLoading();
    
    if (res.statusCode === 200 || res.statusCode === 201) {
      // Save to local storage as backup
      //uni.setStorageSync('personalInfo', JSON.stringify(personalInfo));
      
      uni.showToast({
        title: '保存成功',
        icon: 'success'
      });
    } else {
      uni.showToast({
        title: res.data.error || '保存失败',
        icon: 'none'
      });
    }
  } catch (error) {
    uni.hideLoading();
    uni.showToast({
      title: error.message || '保存失败，请检查网络连接',
      icon: 'none'
    });
    console.error('保存个人信息错误:', error);
  }
};

onMounted(async () => {
  try {
    // First check if we have a token
    const token = uni.getStorageSync('token');
    if (!token) {
      loadLocalData();
      return;
    }
    
    // Show loading
    uni.showLoading({
      title: '加载中...'
    });
    
    // Fetch data from API
    const res = await uni.request({
      url: `${API_BASE_URL}/patient/profile/`,
      method: 'GET',
      header: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      dataType: 'json',
      withCredentials: true
    });
    
    // Hide loading
    uni.hideLoading();
    
    if (res.statusCode === 200 && res.data) {
      // Update personal info with data from server
      Object.assign(personalInfo, res.data);
      
      // Update local storage with latest data
      //uni.setStorageSync('personalInfo', JSON.stringify(personalInfo));
    } else if (res.statusCode === 401) {
      // Handle unauthorized error
      uni.showToast({
        title: '登录已过期，请重新登录',
        icon: 'none'
      });
      // redirect to login page
      uni.reLaunch({
        url: '/pages/login/login'
      });
    } else {
      // If API call fails, fall back to local data
      //loadLocalData();
    }
  } catch (error) {
    uni.hideLoading();
    console.error('获取个人信息失败:', error);
    //loadLocalData();
    uni.showToast({
      title: '获取个人信息失败，请检查网络连接',
      icon: 'none'
    });
  }
});

// const loadLocalData = () => {
//   const savedInfo = uni.getStorageSync('personalInfo');
//   if (savedInfo) {
//     try {
//       const parsedInfo = JSON.parse(savedInfo);
//       Object.assign(personalInfo, parsedInfo);
//     } catch (e) {
//       console.error('解析个人信息失败', e);
//     }
//   }
  
//   // Get phone number from login if available
//   const userPhone = uni.getStorageSync('userPhone');
//   if (userPhone && !personalInfo.phone) {
//     personalInfo.phone = userPhone;
//   }
// };
</script>

<style lang="scss">
.personal-info-container {
  min-height: 100vh;
  padding: 30rpx;
  box-sizing: border-box;
  background-color: #f8f8f8;
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

.info-form {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
  margin-bottom: 40rpx;
  
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
    
    .gender-selector {
      display: flex;
      
      .gender-option {
        flex: 1;
        height: 80rpx;
        background-color: #f5f7fa;
        border-radius: 8rpx;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 20rpx;
        font-size: 28rpx;
        color: #333;
        
        &:last-child {
          margin-right: 0;
        }
        
        &.active {
          background-color: #e6f7ef;
          color: #42b983;
          border: 1px solid #42b983;
        }
      }
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
    
    .bmi-value {
      font-size: 28rpx;
      height: 80rpx;
      display: flex;
      align-items: center;
      
      .bmi-status {
        margin-left: 20rpx;
        font-size: 26rpx;
        padding: 4rpx 16rpx;
        border-radius: 20rpx;
        
        &.underweight {
          background-color: #e6f7ff;
          color: #1890ff;
        }
        
        &.normal {
          background-color: #e6f7ef;
          color: #42b983;
        }
        
        &.overweight {
          background-color: #fff7e6;
          color: #fa8c16;
        }
        
        &.obese {
          background-color: #fff1f0;
          color: #f5222d;
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
}
</style>
