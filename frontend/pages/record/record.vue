<template>
  <view class="container">

    <view class="accordion-container">
      <view v-for="(config, key) in recordConfigs" :key="key" class="accordion-item">
        <view class="accordion-header" @click="toggleAccordion(key)">
          <text class="accordion-title">{{ config.title }}</text>
          <text class="accordion-icon">{{ openSections[key] ? '▼' : '►' }}</text>
        </view>
        <view class="accordion-content" v-if="openSections[key]">
          <view v-if="userRecords[key].length === 0" class="empty-message">
            <text>暂无记录，点击下方的 "+" 添加</text>
          </view>
          <view v-else class="record-list">
            <view v-for="(item, index) in userRecords[key]" :key="index" class="record-item">
              <view class="record-info">
                <view>
                  <text class="record-date">{{ formatDate(item.date) }}</text>
                  <text class="record-date">{{ formatTime(item.date) }}</text>
                </view>
                <view><text class="record-value">{{ formatRecordValue(key, item) }}</text></view>
              </view>
              <view class="record-actions">
                <text class="delete-btn" @click="deleteRecord(key, index)">删除</text>
              </view>
            </view>
          </view>
          <view class="add-record-in-section" @click="openAddModal(config.title)">
            <text class="add-icon">+</text>
            <text>添加{{ config.title }}记录</text>
          </view>
        </view>
      </view>
    </view>

    <view class="modal" v-if="showAddRecordModal">
      <view class="modal-content">
        <view class="modal-header">
          <text class="modal-title">新增 {{ currentRecordType }} 记录</text>
          <text class="modal-close" @click="showAddRecordModal = false">×</text>
        </view>

        <view class="modal-body">
          <view class="form-item">
            <text class="form-label">日期</text>
            <picker mode="date" :value="selectedDate" :start="startDate" :end="endDate" @change="onDateChange">
              <view class="picker-value">{{ selectedDate || '请选择日期' }}</view>
            </picker>
          </view>

          <view class="form-item">
            <text class="form-label">时间</text>
            <picker mode="time" :value="selectedTime" @change="onTimeChange">
              <view class="picker-value">{{ selectedTime || '请选择时间' }}</view>
            </picker>
          </view>

          <!-- 动态生成表单字段 -->
          <view v-for="(field, index) in currentFormFields" :key="index">
            <view class="form-item">
              <text class="form-label">{{ field.label }}</text>

              <!-- 文本输入 -->
              <input v-if="field.type === 'text'" type="text" v-model="dynamicForm[field.key]"
                :placeholder="field.placeholder" class="input" />

              <!-- 数字输入 -->
              <input v-if="field.type === 'digit'" type="digit" v-model="dynamicForm[field.key]"
                :placeholder="field.placeholder" class="input" />

              <!-- 选择器 -->
              <picker v-if="field.type === 'picker'" :range="field.options"
                @change="(e) => handlePickerChange(e, field.key)" class="picker">
                <view class="picker-value">
                  {{ dynamicForm[field.key] || field.placeholder }}
                </view>
              </picker>

              <view v-if="field.type === 'radio'" class="radio-group">
                <view class="radio-options">
                  <view v-for="option in field.options" :key="option" class="radio-option"
                    :class="{ 'radio-selected': dynamicForm[field.key] === option }"
                    @click="dynamicForm[field.key] = option">
                    <text>{{ option }}</text>
                  </view>
                </view>
              </view>

              <!-- 滑块 -->
              <slider v-if="field.type === 'slider'" 
                :value="Number(dynamicForm[field.key])" 
                :min="field.min" 
                :max="field.max"
                show-value 
                @change="(e) => onSliderChange(e, field.key)"
                class="slider" />

              <!-- 文本域 -->
              <textarea v-if="field.type === 'textarea'" v-model="dynamicForm[field.key]"
                :placeholder="field.placeholder" class="textarea" />
            </view>
          </view>
        </view>

        <view class="modal-footer">
          <button class="cancel-btn" @click="showAddRecordModal = false">取消</button>
          <button class="confirm-btn" @click="addRecord">确认添加</button>
        </view>
      </view>
    </view>

    <LogoutButton />
  </view>
</template>

<script setup>
import {
  ref,
  reactive,
  computed,
  onMounted
} from 'vue';
import {
  recordConfigs
} from '@/utils/record.config.js';
import { API_BASE_URL } from '@/utils/config.js';
import LogoutButton from '@/components/LogoutButton.vue';

// 用于反向查找键
const getTitleToKeyMap = computed(() => {
  const map = {};
  Object.entries(recordConfigs).forEach(([key, config]) => {
    map[config.title] = key;
  });
  return map;
});

// 控制手风琴展开状态
const openSections = reactive({
  weight: true,
  mainFood: false,
  waterIntake: false,
  purineFood: false,
  uricAcid: false,
  urinePH: false,
  liverFunction: false,
  kidneyFunction: false,
  bloodSugar: false,
  bloodPressure: false,
  bloodLipid: false,
  attack: false,
  tophi: false,
  surgery: false,
  jointFunction: false
});

// 用户记录数据 - 初始为空
const userRecords = reactive({
  weight: [],
  mainFood: [],
  waterIntake: [],
  purineFood: [],
  uricAcid: [],
  urinePH: [],
  liverFunction: [],
  kidneyFunction: [],
  bloodSugar: [],
  bloodPressure: [],
  bloodLipid: [],
  attack: [],
  tophi: [],
  surgery: [],
  jointFunction: []
});

// 控制新增记录弹窗的显示
const showAddRecordModal = ref(false);
const currentRecordType = ref('');
const selectedDate = ref(formatDate(new Date()));
const selectedTime = ref(formatTime(new Date()));
const startDate = '2020-01-01';
const endDate = '2030-12-31';
const dynamicForm = reactive({});
const currentFormFields = ref([]);
const isLoading = ref(false);

// 切换手风琴面板
const toggleAccordion = (section) => {
  openSections[section] = !openSections[section];
};

// 打开模态框并设置类型
const openAddModal = (recordType) => {
  currentRecordType.value = recordType;
  
  // Set current date and time as initial values
  const now = new Date();
  selectedDate.value = formatDate(now);
  selectedTime.value = formatTime(now);
  
  // Clear form
  Object.keys(dynamicForm).forEach(key => {
    delete dynamicForm[key];
  });

  // Set current form fields
  const recordKey = getTitleToKeyMap.value[recordType];
  currentFormFields.value = recordConfigs[recordKey].fields;

  // Set slider default values
  currentFormFields.value.forEach(field => {
    if (field.type === 'slider') {
      // Make sure the slider value is properly initialized as a number
      dynamicForm[field.key] = field.initial !== undefined ? Number(field.initial) : 
                              (field.min !== undefined ? Number(field.min) : 0);
    }
  });

  showAddRecordModal.value = true;
};

// Format date to YYYY-MM-DD
function formatDate(date) {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

// Format time to HH:mm
function formatTime(date) {
  const d = new Date(date);
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  return `${hours}:${minutes}`;
}

// Handle date picker change
function onDateChange(e) {
  selectedDate.value = e.detail.value;
}

// Handle time picker change
function onTimeChange(e) {
  selectedTime.value = e.detail.value;
}

// 处理选择器变化
const handlePickerChange = (e, key) => {
  const index = e.detail.value;
  // 找到字段配置
  const field = currentFormFields.value.find(f => f.key === key);
  if (field && field.options) {
    dynamicForm[key] = field.options[index];
  }
};

// Handle slider change
function onSliderChange(e, key) {
  // Ensure slider value is stored as a number
  dynamicForm[key] = Number(e.detail.value);
}

// 格式化记录值显示
const formatRecordValue = (recordKey, item) => {
  return recordConfigs[recordKey].formatter(item);
};

// 加载记录数据
const loadRecords = async () => {
  try {
    isLoading.value = true;
    
    // Get token from storage
    const token = uni.getStorageSync('token');
    if (!token) {
      uni.redirectTo({ url: '/pages/login/login' });
      return;
    }
    
    console.log('Using token:', token); // Debug log
    
    const res = await uni.request({
      url: `${API_BASE_URL}/records/`,
      method: 'GET',
      header: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      withCredentials: true
    });
    
    console.log('API response:', res.statusCode, res.data); // Debug log
    
    if (res.statusCode === 200 && res.data) {
      // Clear existing records
      Object.keys(userRecords).forEach(key => {
        userRecords[key] = [];
      });
      
      // Process and add records from API
      Object.entries(res.data).forEach(([recordType, records]) => {
        if (userRecords[recordType]) {
          records.forEach(record => {
            try {
              // Ensure date is properly converted to a Date object
              const recordDate = new Date(record.date);
              
              // Check if date is valid before adding
              if (!isNaN(recordDate.getTime())) {
                userRecords[recordType].push({
                  id: record.id,
                  date: recordDate,
                  ...record
                });
              } else {
                console.error('Invalid date format:', record.date);
              }
            } catch (err) {
              console.error('Error processing record:', err, record);
            }
          });
          
          // Sort by date (newest first) with error handling
          if (userRecords[recordType].length > 0) {
            try {
              userRecords[recordType].sort((a, b) => {
                // Ensure both dates are valid
                const dateA = a.date instanceof Date ? a.date.getTime() : 0;
                const dateB = b.date instanceof Date ? b.date.getTime() : 0;
                return dateB - dateA;
              });
            } catch (err) {
              console.error('Error sorting records:', err);
            }
          }
        }
      });
    } else if (res.statusCode === 401) {
      // Handle unauthorized error
      console.error('Authentication failed. Redirecting to login.');
      uni.showToast({
        title: '登录已过期，请重新登录',
        icon: 'none'
      });
      
      // Clear token and redirect to login
      uni.removeStorageSync('token');
      uni.removeStorageSync('isLoggedIn');
      
      setTimeout(() => {
        uni.redirectTo({ url: '/pages/login/login' });
      }, 1500);
    }
  } catch (error) {
    console.error('加载记录失败:', error);
    uni.showToast({
      title: '加载记录失败，请检查网络连接',
      icon: 'none'
    });
  } finally {
    isLoading.value = false;
  }
};

// 添加记录
const addRecord = async () => {
  const recordKey = getTitleToKeyMap.value[currentRecordType.value];
  if (!recordKey) return;

  // Combine date and time
  const dateTimeStr = `${selectedDate.value}T${selectedTime.value}:00`;
  const recordDate = new Date(dateTimeStr);

  // Validate date
  if (isNaN(recordDate.getTime())) {
    uni.showToast({
      title: '请选择有效的日期和时间',
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
    
    // Prepare data for API
    const apiData = {
      record_type: recordKey,
      date: recordDate.toISOString(),
      data: { ...dynamicForm }
    };
    
    console.log('Sending data to API:', apiData); // Debug log
    
    // Send data to backend
    const res = await uni.request({
      url: `${API_BASE_URL}/records/`,
      method: 'POST',
      data: apiData,
      header: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      withCredentials: true
    });
    
    console.log('API response:', res.statusCode, res.data); // Debug log
    
    // Hide loading
    uni.hideLoading();
    
    if (res.statusCode === 201) {
      // Create new record for local display
      const newRecord = {
        id: res.data.id,
        date: recordDate,
        ...dynamicForm
      };

      // Add to records
      userRecords[recordKey].push(newRecord);
      
      // Sort records by date (newest first)
      userRecords[recordKey].sort(function(a, b) {
        // Safely get timestamps for comparison
        var dateA = a.date instanceof Date ? a.date.getTime() : 0;
        var dateB = b.date instanceof Date ? b.date.getTime() : 0;
        return dateB - dateA;
      });

      // Close modal
      showAddRecordModal.value = false;

      // Show success message
      uni.showToast({
        title: '添加成功',
        icon: 'success'
      });
    } else if (res.statusCode === 401) {
      // Handle unauthorized error
      uni.showToast({
        title: '登录已过期，请重新登录',
        icon: 'none'
      });
      
      setTimeout(() => {
        uni.redirectTo({ url: '/pages/login/login' });
      }, 1500);
    } else {
      throw new Error(res.data ? res.data.error : '保存失败');
    }
  } catch (error) {
    uni.hideLoading();
    uni.showToast({
      title: error.message || '保存失败，请检查网络连接',
      icon: 'none'
    });
    console.error('保存记录错误:', error);
  }
};

// 删除记录
const deleteRecord = (recordKey, index) => {
  const record = userRecords[recordKey][index];
  if (!record || !record.id) {
    uni.showToast({
      title: '记录ID不存在',
      icon: 'none'
    });
    return;
  }
  
  uni.showModal({
    title: '确认删除',
    content: '确定要删除这条记录吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          // Show loading
          uni.showLoading({
            title: '删除中...'
          });
          
          // Get token from storage
          const token = uni.getStorageSync('token');
          if (!token) {
            throw new Error('登录已过期，请重新登录');
          }
          
          // Send delete request to backend
          const apiRes = await uni.request({
            url: `${API_BASE_URL}/records/${record.id}/`,
            method: 'DELETE',
            header: {
              'Authorization': `Bearer ${token}`
            }
          });
          
          // Hide loading
          uni.hideLoading();
          
          if (apiRes.statusCode === 204) {
            // Remove from local records
            userRecords[recordKey].splice(index, 1);
            
            // Show success message
            uni.showToast({
              title: '删除成功',
              icon: 'success'
            });
          } else {
            throw new Error(apiRes.data ? apiRes.data.error : '删除失败');
          }
        } catch (error) {
          uni.hideLoading();
          uni.showToast({
            title: error.message || '删除失败，请检查网络连接',
            icon: 'none'
          });
          console.error('删除记录错误:', error);
        }
      }
    }
  });
};

// 页面加载时获取记录
onMounted(() => {
  const token = uni.getStorageSync('token');
  if (!token) {
    console.log('No token found, redirecting to login');
    uni.redirectTo({ url: '/pages/login/login' });
    return;
  }
  
  console.log('Token found, loading records');
  loadRecords();
});
</script>


<style lang="scss" scoped>
.container {
  padding: 15px;
  background-color: #f7f7f7;
}

.accordion-container {
  background: #fff;
  border-radius: 8px;
}

.accordion-item {
  border-bottom: 1px solid #eee;
  
  &:last-child {
    border-bottom: none;
  }
}

.accordion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #fff;
}

.accordion-title {
  font-size: 16px;
  color: #333;
}

.accordion-icon {
  color: #666;
  font-size: 12px;
}

.accordion-content {
  background: #fff;
  padding: 0 15px;
}

.empty-message {
  padding: 20px 0;
  text-align: center;
  color: #999;
  font-size: 14px;
}

.record-list {
  padding: 10px 0;
}

.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f5f5f5;
  
  &:last-child {
    border-bottom: none;
  }
}

.record-info {
  flex: 1;
}

.record-date {
  font-size: 14px;
  color: #666;
  margin-right: 10px;
}

.record-value {
  font-size: 14px;
  color: #333;
}

.record-actions {
  padding-left: 15px;
}

.delete-btn {
  color: #ff5a5f;
  font-size: 14px;
}

.add-record-in-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 15px 0;
  color: #2979ff;
  font-size: 14px;
}

.add-icon {
  margin-right: 5px;
  font-size: 16px;
}

// Modal styles
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal-content {
  width: 85%;
  max-height: 80vh;
  overflow-y: auto;
  background-color: #fff;
  border-radius: 12px;
  padding: 20px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.modal-close {
  font-size: 20px;
  color: #999;
  padding: 5px;
}

.form-item {
  margin-bottom: 15px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #333;
}

.picker-value {
  height: 40px;
  line-height: 40px;
  padding: 0 12px;
  background-color: #f7f7f7;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
}

.input {
  height: 40px;
  line-height: 40px;
  padding: 0 12px;
  background-color: #f7f7f7;
  border-radius: 4px;
  font-size: 14px;
}

.textarea {
  width: 100%;
  height: 100px;
  padding: 12px;
  background-color: #f7f7f7;
  border-radius: 4px;
  font-size: 14px;
}

.radio-group {
  .radio-options {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  .radio-option {
    padding: 8px 15px;
    border-radius: 4px;
    background-color: #f7f7f7;
    font-size: 14px;
    color: #333;

    &.radio-selected {
      background-color: #2979ff;
      color: #fff;
    }
  }
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.cancel-btn,
.confirm-btn {
  padding: 8px 20px;
  border-radius: 4px;
  font-size: 14px;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #666;
}

.confirm-btn {
  background-color: #2979ff;
  color: #fff;
}

// Slider customization
.slider {
  margin: 15px 0;
}
</style>
