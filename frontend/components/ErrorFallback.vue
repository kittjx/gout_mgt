<template>
  <view class="error-fallback">
    <view class="error-icon">⚠️</view>
    <text class="error-title">{{ title || '页面加载出错' }}</text>
    <text class="error-message">{{ message || '请刷新页面或稍后再试' }}</text>
    <button class="retry-button" @click="$emit('retry')">重试</button>
  </view>
</template>

<script setup>
defineProps({
  title: String,
  message: String
});

defineEmits(['retry']);
</script>

<style scoped>
.error-fallback {
  padding: 30px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  border-radius: 8px;
  margin: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.error-icon {
  font-size: 40px;
  margin-bottom: 15px;
}

.error-title {
  font-size: 18px;
  font-weight: 500;
  color: #333;
  margin-bottom: 10px;
}

.error-message {
  font-size: 14px;
  color: #666;
  text-align: center;
  margin-bottom: 20px;
}

.retry-button {
  background-color: #2979ff;
  color: #fff;
  padding: 8px 20px;
  border-radius: 4px;
  font-size: 14px;
}
</style>