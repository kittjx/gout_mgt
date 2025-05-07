<template>
  <view class="login-container">
    <view class="login-header">
      <image class="logo" src="/static/logo.png" mode="aspectFit"></image>
      <text class="title">痛风患者信息管理系统</text>
    </view>

    <view class="login-form">
      <view class="form-item">
        <text class="label">手机号</text>
        <input class="input" type="number" placeholder="请输入手机号" maxlength="11" v-model="phone" />
      </view>

      <view class="form-item">
        <text class="label">密码</text>
        <view class="input-wrapper">
          <input class="input" placeholder="请输入密码" :password="!showPassword" v-model="password" />
          <text class="password-toggle" @tap="togglePasswordVisibility">{{ showPassword ? '隐藏' : '显示' }}</text>
        </view>
      </view>

      <view class="login-options">
        <view class="remember-pwd">
          <checkbox :checked="rememberPwd" @tap="rememberPwd = !rememberPwd" color="#42b983" />
          <text @tap="rememberPwd = !rememberPwd">记住密码</text>
        </view>
        <text class="forget-pwd" @tap="goToResetPassword">忘记密码?</text>
      </view>

      <button class="login-btn" @tap="handleLogin" :disabled="isLoading">
        {{ isLoading ? '登录中...' : '登录' }}
      </button>

      <view class="register-link">
        <text>还没有账号? </text>
        <text class="link" @tap="goToRegister">立即注册</text>
      </view>
    </view>
  </view>
</template>

<script setup>
  import {
    ref,
    onMounted
  } from 'vue';
  
  import { API_BASE_URL } from '@/utils/config.js';

  // 响应式状态
  const phone = ref('');
  const password = ref('');
  const showPassword = ref(false);
  const rememberPwd = ref(false);
  const isLoading = ref(false);
  
  // 显示/隐藏密码
  const togglePasswordVisibility = () => {
    showPassword.value = !showPassword.value;
    console.log('show password: ', showPassword.value);
  };

  // 登录处理
  const handleLogin = async () => {
    if (!phone.value) {
      uni.showToast({
        title: '请输入手机号',
        icon: 'none'
      });
      return;
    }

    if (!password.value) {
      uni.showToast({
        title: '请输入密码',
        icon: 'none'
      });
      return;
    }

    try {
      isLoading.value = true;

      const res = await uni.request({
        url: `${API_BASE_URL}/accounts/login/`,
        method: 'POST',
        data: {
          phone: phone.value,
          password: password.value
        },
        dataType: 'json'
      });

      if (res.statusCode === 200) {
        // 保存用户信息和Token
        const token = res.data.token;
        uni.setStorageSync('token', token);
        uni.setStorageSync('isLoggedIn', true);
        uni.setStorageSync('userPhone', phone.value);

        // 如果选择记住密码，保存密码
        if (rememberPwd.value) {
          uni.setStorageSync('savedPhone', phone.value);
          uni.setStorageSync('savedPassword', password.value);
        } else {
          uni.removeStorageSync('savedPassword');
        }

        uni.showToast({
          title: '登录成功',
          icon: 'success'
        });

        // 跳转到个人信息页面
        setTimeout(() => {
          uni.switchTab({
            url: '/pages/personal/personal'
          });
        }, 1500);
      } else {
        // 处理登录失败
        uni.showToast({
          title: res.data.error || '账号或密码错误',
          icon: 'none'
        });
      }
    } catch (error) {
      uni.showToast({
        title: '登录失败，请检查网络连接',
        icon: 'none'
      });
    } finally {
      isLoading.value = false;
    }
  };

  // 跳转到注册页面
  const goToRegister = () => {
    uni.navigateTo({
      url: '/pages/register/register'
    });
  };

  // 跳转到重置密码页面
  const goToResetPassword = () => {
    uni.showToast({
      title: '忘记密码功能开发中',
      icon: 'none'
    });
  };
  
  
  // 页面加载时，检查是否有保存的账号密码
  onMounted(() => {
    const savedPhone = uni.getStorageSync('savedPhone');
    const savedPassword = uni.getStorageSync('savedPassword');
    
    if (savedPhone) {
      phone.value = savedPhone;
      rememberPwd.value = true;
    }
    
    if (savedPassword) {
      password.value = savedPassword;
    }
  });
  
</script>

<style lang="scss">
  .login-container {
    min-height: 100vh;
    padding: 60rpx;
    box-sizing: border-box;
    background-color: #f8f8f8;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .login-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 80rpx;

    .logo {
      width: 180rpx;
      height: 180rpx;
      margin-bottom: 30rpx;
    }

    .title {
      font-size: 36rpx;
      font-weight: bold;
      color: #333;
    }
  }

  .login-form {
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

      .input-wrapper {
        position: relative;
        width: 100%;
      }
      
      .input {
        width: 100%;
        height: 80rpx;
        background-color: #f5f7fa;
        border-radius: 8rpx;
        padding: 0 100rpx 0 20rpx; /* Add right padding to make room for the toggle */
        font-size: 28rpx;
        color: #333;
        box-sizing: border-box;
      }
      
      .password-toggle {
        position: absolute;
        right: 20rpx;
        top: 50%;
        transform: translateY(-50%);
        font-size: 26rpx;
        color: #42b983;
        z-index: 2; /* Ensure it's above the input */
      }
    }

    .login-options {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 40rpx;

      .remember-pwd {
        display: flex;
        align-items: center;
        font-size: 26rpx;
        color: #666;
      }

      .forget-pwd {
        font-size: 26rpx;
        color: #42b983;
      }
    }

    .login-btn {
      width: 100%;
      height: 90rpx;
      background-color: #42b983;
      color: #fff;
      border-radius: 45rpx;
      font-size: 32rpx;
      font-weight: bold;
      line-height: 90rpx;
      margin-bottom: 30rpx;
    }

    .register-link {
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
