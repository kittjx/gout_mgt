<template>
  <view class="register-container">
    <view class="header">
      <text class="title">注册账号</text>
      <text class="subtitle">填写信息，创建您的账号</text>
    </view>
    
    <view class="register-form">
      <view class="form-item">
        <text class="label">手机号</text>
        <input 
          class="input" 
          type="number" 
          placeholder="请输入手机号" 
          maxlength="11"
          v-model="phone"
        />
      </view>
      
      <view class="form-item verification">
        <text class="label">验证码</text>
        <input 
          class="input verification-input" 
          type="number" 
          placeholder="请输入验证码" 
          maxlength="6"
          v-model="verificationCode"
        />
        <button 
          class="verification-btn" 
          :disabled="counting || isLoadingVerificationCode" 
          @tap="sendVerificationCode"
        >
          {{ counting ? `${countdown}s后重新获取` : (isLoadingVerificationCode ? '发送中...' : '获取验证码') }}
        </button>
      </view>
      
      <view class="form-item">
        <text class="label">设置密码</text>
        <input 
          class="input" 
          :type="showPassword ? 'text' : 'password'" 
          placeholder="请设置密码，不少于6位" 
          v-model="password"
        />
        <text class="password-toggle" @tap="togglePasswordVisibility">
          {{ showPassword ? '隐藏' : '显示' }}
        </text>
      </view>
      
      <view class="form-item">
        <text class="label">确认密码</text>
        <input 
          class="input" 
          :type="showConfirmPassword ? 'text' : 'password'" 
          placeholder="请再次输入密码" 
          v-model="confirmPassword"
        />
        <text class="password-toggle" @tap="toggleConfirmPasswordVisibility">
          {{ showConfirmPassword ? '隐藏' : '显示' }}
        </text>
      </view>
      
      <view class="agreement">
        <checkbox :checked="agreeTerms" @tap="agreeTerms = !agreeTerms" color="#42b983" />
        <text @tap="agreeTerms = !agreeTerms">
          我已阅读并同意
          <text class="terms-link" @tap.stop="showTerms">《用户协议》</text>
          和
          <text class="terms-link" @tap.stop="showPrivacy">《隐私政策》</text>
        </text>
      </view>
      
      <button 
        class="register-btn" 
        :class="{ disabled: !canRegister || isLoading }" 
        :disabled="!canRegister || isLoading" 
        @tap="handleRegister"
      >
        {{ isLoading ? '注册中...' : '注册' }}
      </button>
      
      <view class="login-link">
        <text>已有账号? </text>
        <text class="link" @tap="goToLogin">立即登录</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue';

import { API_BASE_URL } from '@/utils/config.js';

// 响应式状态
const phone = ref('');
const verificationCode = ref('');
const password = ref('');
const confirmPassword = ref('');
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const agreeTerms = ref(false);
const counting = ref(false);
const countdown = ref(60);
const isLoading = ref(false);
const isLoadingVerificationCode = ref(false);


// 计算属性：是否可以注册
const canRegister = computed(() => {
  return (
    phone.value.length === 11 &&
    verificationCode.value.length === 6 &&
    password.value.length >= 6 &&
    password.value === confirmPassword.value &&
    agreeTerms.value
  );
});

// 显示/隐藏密码
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

// 显示/隐藏确认密码
const toggleConfirmPasswordVisibility = () => {
  showConfirmPassword.value = !showConfirmPassword.value;
};

// 发送验证码
// const sendVerificationCode = () => {
//   if (phone.value.length !== 11) {
//     uni.showToast({
//       title: '请输入正确的手机号',
//       icon: 'none'
//     });
//     return;
//   }
  
//   // 开始倒计时
//   counting.value = true;
//   const timer = setInterval(() => {
//     countdown.value--;
//     if (countdown.value <= 0) {
//       clearInterval(timer);
//       counting.value = false;
//       countdown.value = 60;
//     }
//   }, 1000);
  
//   // 模拟发送验证码
//   uni.showToast({
//     title: '验证码已发送',
//     icon: 'success'
//   });
// };
const sendVerificationCode = async () => {
  if (phone.value.length !== 11) {
    uni.showToast({
      title: '请输入正确的手机号',
      icon: 'none'
    });
    return;
  }
  
  try {
    isLoadingVerificationCode.value = true;
    
    const res = await uni.request({
      url: `${API_BASE_URL}/accounts/verification-code/`,
      method: 'POST',
      data: {
        phone: phone.value
      },
      dataType: 'json'
    });
    
    //const [error, res] = response;
    
    // if (error) {
    //   throw new Error('网络请求失败');
    // }
    
    if (res.statusCode === 200) {
      // 开始倒计时
      counting.value = true;
      const timer = setInterval(() => {
        countdown.value--;
        if (countdown.value <= 0) {
          clearInterval(timer);
          counting.value = false;
          countdown.value = 60;
        }
      }, 1000);
      
      // 显示验证码 (在生产环境中应该通过短信发送)
      if (res.data.code) {
        uni.showModal({
          title: '验证码',
          content: `您的验证码是：${res.data.code}`,
          showCancel: false
        });
      } else {
        uni.showToast({
          title: '验证码已发送',
          icon: 'success'
        });
      }
    } else {
      uni.showToast({
        title: res.data.error || '获取验证码失败',
        icon: 'none'
      });
    }
  } catch (error) {
    uni.showToast({
      title: '获取验证码失败，请检查网络连接',
      icon: 'none'
    });
    console.error('获取验证码错误:', error);
  } finally {
    isLoadingVerificationCode.value = false;
  }
};

// 注册处理
// const handleRegister = () => {
//   if (!canRegister.value) return;
  
//   // 模拟注册
//   uni.showLoading({
//     title: '注册中...'
//   });
  
//   setTimeout(() => {
//     uni.hideLoading();
//     uni.showToast({
//       title: '注册成功',
//       icon: 'success'
//     });
    
//     // 跳转到登录页面
//     setTimeout(() => {
//       uni.navigateBack();
//     }, 1500);
//   }, 2000);
// };
const handleRegister = async () => {
  if (!canRegister.value) return;
  
  try {
    isLoading.value = true;
    
    const res = await uni.request({
      url: `${API_BASE_URL}/accounts/register/`,
      method: 'POST',
      data: {
        phone: phone.value,
        password: password.value,
        verification_code: verificationCode.value
      },
      dataType: 'json'
    });
    
    // const [error, res] = response;
    
    // if (error) {
    //   throw new Error('网络请求失败');
    // }
    
    if (res.statusCode === 201) {
      uni.showToast({
        title: '注册成功',
        icon: 'success'
      });
      
      // 存储token
      if (res.data.token) {
        uni.setStorageSync('token', res.data.token);
        uni.setStorageSync('isLoggedIn', true);
        uni.setStorageSync('userPhone', phone.value);
      }
      
      // 跳转到登录页面或个人信息页面
      setTimeout(() => {
        if (res.data.token) {
          // 如果已经登录，直接跳转到个人信息页面
          uni.switchTab({
            url: '/pages/personal/personal'
          });
        } else {
          // 否则跳转到登录页面
          uni.navigateBack();
        }
      }, 1500);
    } else {
      // 处理注册失败
      uni.showToast({
        title: res.data.error || '注册失败',
        icon: 'none'
      });
    }
  } catch (error) {
    uni.showToast({
      title: '注册失败，请检查网络连接',
      icon: 'none'
    });
    console.error('注册错误:', error);
  } finally {
    isLoading.value = false;
  }
};

// 跳转到登录页面
const goToLogin = () => {
  uni.navigateBack();
};

// 显示用户协议
const showTerms = () => {
  uni.showToast({
    title: '用户协议功能开发中',
    icon: 'none'
  });
};
// const showTerms = () => {
//   uni.navigateTo({
//     url: '/pages/terms/terms'
//   });
// };

// 显示隐私政策
const showPrivacy = () => {
  uni.showToast({
    title: '隐私政策功能开发中',
    icon: 'none'
  });
};
// const showPrivacy = () => {
//   uni.navigateTo({
//     url: '/pages/privacy/privacy'
//   });
// };
</script>

<style lang="scss">
.register-container {
  min-height: 100vh;
  padding: 60rpx;
  box-sizing: border-box;
  background-color: #f8f8f8;
}

.header {
  margin-bottom: 60rpx;
  
  .title {
    font-size: 44rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
    display: block;
  }
  
  .subtitle {
    font-size: 28rpx;
    color: #666;
  }
}

.register-form {
  background-color: #fff;
  border-radius: 20rpx;
  padding: 40rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
  
  .form-item {
    position: relative;
    margin-bottom: 40rpx;
    
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
    
    .password-toggle {
      position: absolute;
      right: 20rpx;
      bottom: 24rpx;
      font-size: 26rpx;
      color: #42b983;
    }
  }
  
  .verification {
    display: flex;
    flex-direction: column;
    
    .verification-input {
      width: 100%;
    }
    
    .verification-btn {
      position: absolute;
      right: 0;
      bottom: 0;
      height: 80rpx;
      line-height: 80rpx;
      font-size: 26rpx;
      color: #42b983;
      background-color: transparent;
      padding: 0 20rpx;
      
      &::after {
        border: none;
      }
      
      &[disabled] {
        color: #999;
      }
    }
  }
  
  .agreement {
    display: flex;
    align-items: center;
    margin-bottom: 40rpx;
    font-size: 26rpx;
    color: #666;
    
    .terms-link {
      color: #42b983;
    }
  }
  
  .register-btn {
    width: 100%;
    height: 90rpx;
    background-color: #42b983;
    color: #fff;
    border-radius: 45rpx;
    font-size: 32rpx;
    font-weight: bold;
    line-height: 90rpx;
    margin-bottom: 30rpx;
    
    &.disabled {
      background-color: #c8e6d7;
    }
  }
  
  .login-link {
    text-align: center;
    font-size: 26rpx;
    color: #666;
    
    .link {
      color: #42b983;
      font-weight: bold;
    }
  }
}
</style>