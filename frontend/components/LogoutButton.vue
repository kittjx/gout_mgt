<template>
  <button class="logout-btn" @tap="handleLogout">退出登录</button>
</template>

<script setup>
const handleLogout = () => {
  uni.showModal({
    title: '确认退出',
    content: '确定要退出登录吗？',
    confirmColor: '#ff4d4f',
    success: (res) => {
      if (res.confirm) {
        try {
          // Clear all authentication related storage
          uni.removeStorageSync('token');
          uni.removeStorageSync('isLoggedIn');
          uni.removeStorageSync('userPhone');
          uni.removeStorageSync('savedPassword');
          uni.removeStorageSync('savedPhone');
          
          // Show success message
          uni.showToast({
            title: '已退出登录',
            icon: 'success',
            duration: 1500
          });
          
          // Redirect to login page after a short delay
          setTimeout(() => {
            uni.reLaunch({
              url: '/pages/login/login'
            });
          }, 1500);
        } catch (error) {
          console.error('退出登录错误:', error);
          uni.showToast({
            title: '退出登录失败',
            icon: 'none'
          });
        }
      }
    }
  });
};
</script>

<style lang="scss">
.logout-btn {
  width: 100%;
  height: 90rpx;
  background-color: #fff;
  color: #ff4d4f;
  border: 1px solid #ff4d4f;
  border-radius: 45rpx;
  font-size: 32rpx;
  font-weight: bold;
  line-height: 90rpx;
  margin-top: 30rpx;
  
  &:active {
    background-color: #fff1f0;
  }
}
</style>