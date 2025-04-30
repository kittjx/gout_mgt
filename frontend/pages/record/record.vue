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
                <text class="record-date">{{ formatDate(item.date) }}</text>
                <text class="record-value">{{ formatRecordValue(key, item) }}</text>
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
            <text class="form-label">记录时间</text>
            <uni-datetime-picker type="datetime" v-model="selectedDateTime" start="2020-01-01 00:00:00"
              end="2030-12-31 23:59:59" return-type="string" />
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
              <slider v-if="field.type === 'slider'" v-model="dynamicForm[field.key]" :min="field.min" :max="field.max"
                show-value class="slider" />

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
  </view>
</template>

<script setup>
  import {
    ref,
    reactive,
    computed
  } from 'vue';
  import {
    recordConfigs
  } from '@/utils/record.config.js';


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

  // 用户记录数据 - 初始示例数据
  const userRecords = reactive({
    weight: [{
        date: new Date('2025-04-18T10:30:00'),
        value: 75.5
      },
      {
        date: new Date('2025-04-15T09:00:00'),
        value: 76.2
      }
    ],
    mainFood: [{
      date: new Date('2025-04-19T12:00:00'),
      name: '米饭',
      amount: '1碗'
    }],
    waterIntake: [{
      date: new Date('2025-04-20T14:00:00'),
      amount: 2000
    }],
    purineFood: [],
    uricAcid: [{
      date: new Date('2025-04-10T08:00:00'),
      value: 420,
      method: '血液检测'
    }],
    urinePH: [],
    liverFunction: [],
    kidneyFunction: [],
    bloodSugar: [],
    bloodPressure: [],
    bloodLipid: [],
    attack: [{
      date: new Date('2025-04-05T20:00:00'),
      duration: 6,
      painScore: 8
    }],
    tophi: [],
    surgery: [],
    jointFunction: []
  });

  // 控制新增记录弹窗的显示
  const showAddRecordModal = ref(false);
  const currentRecordType = ref('');
  const selectedDateTime = ref('');
  const dynamicForm = reactive({});
  const currentFormFields = ref([]);

  // 切换手风琴面板
  const toggleAccordion = (section) => {
    openSections[section] = !openSections[section];
  };

  // 打开模态框并设置类型
  const openAddModal = (recordType) => {
    currentRecordType.value = recordType;
    selectedDateTime.value = getCurrentFormattedDateTimeString();

    // 清空表单
    Object.keys(dynamicForm).forEach(key => {
      delete dynamicForm[key];
    });

    // 设置当前表单字段
    const recordKey = getTitleToKeyMap.value[recordType];
    currentFormFields.value = recordConfigs[recordKey].fields;

    // 设置滑块默认值
    currentFormFields.value.forEach(field => {
      if (field.type === 'slider') {
        dynamicForm[field.key] = field.min + Math.floor((field.max - field.min) / 2);
      }
    });

    showAddRecordModal.value = true;
  };

  // 获取当前格式化日期时间字符串
  const getCurrentFormattedDateTimeString = () => {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  };

  // 处理选择器变化
  const handlePickerChange = (e, key) => {
    const index = e.detail.value;
    // 找到字段配置
    const field = currentFormFields.value.find(f => f.key === key);
    if (field && field.options) {
      dynamicForm[key] = field.options[index];
    }
  };

  // 格式化记录值显示
  const formatRecordValue = (recordKey, item) => {
    return recordConfigs[recordKey].formatter(item);
  };

  // 添加记录
  const addRecord = () => {
    if (!selectedDateTime.value) {
      uni.showToast({
        title: '请选择记录时间',
        icon: 'none'
      });
      return;
    }

    const recordDate = new Date(selectedDateTime.value.replace(/-/g, "/"));

    if (isNaN(recordDate.getTime())) {
      uni.showToast({
        title: '无效的日期时间格式',
        icon: 'none'
      });
      console.error("Invalid date constructed from picker:", selectedDateTime.value);
      return;
    }

    const recordKey = getTitleToKeyMap.value[currentRecordType.value];
    if (!recordKey) {
      console.error("Invalid record type selected:", currentRecordType.value);
      uni.showToast({
        title: '无效的记录类型',
        icon: 'none'
      });
      return;
    }

    const config = recordConfigs[recordKey];

    // 验证
    if (config.validator(dynamicForm)) {
      // 处理数据并添加记录
      const newRecordData = config.processor(dynamicForm, recordDate);
      userRecords[recordKey].unshift(newRecordData);

      // 排序记录
      userRecords[recordKey].sort((a, b) => b.date.getTime() - a.date.getTime());

      showAddRecordModal.value = false;

      // 清空表单
      Object.keys(dynamicForm).forEach(key => {
        delete dynamicForm[key];
      });

      currentRecordType.value = '';
      selectedDateTime.value = '';
      currentFormFields.value = [];
    } else {
      uni.showToast({
        title: '请填写完整的记录信息',
        icon: 'none'
      });
    }
  };

  // 删除记录
  const deleteRecord = (recordKey, index) => {
    uni.showModal({
      title: '确认删除',
      content: '确定要删除这条记录吗？',
      success: (res) => {
        if (res.confirm) {
          if (userRecords[recordKey] && userRecords[recordKey][index] !== undefined) {
            userRecords[recordKey].splice(index, 1);
          } else {
            console.error("Could not find record to delete at key:", recordKey, "index:", index);
            uni.showToast({
              title: '删除失败',
              icon: 'none'
            });
          }
        }
      }
    });
  };

  // 格式化日期
  const formatDate = (date) => {
    if (!(date instanceof Date)) {
      const parsedDate = new Date(date);
      if (isNaN(parsedDate.getTime())) return '无效日期';
      date = parsedDate;
    }

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);

    const isToday = date.getFullYear() === today.getFullYear() &&
      date.getMonth() === today.getMonth() &&
      date.getDate() === today.getDate();

    const isYesterday = date.getFullYear() === yesterday.getFullYear() &&
      date.getMonth() === yesterday.getMonth() &&
      date.getDate() === yesterday.getDate();

    if (isToday) {
      return `今天 ${hours}:${minutes}`;
    } else if (isYesterday) {
      return `昨天 ${hours}:${minutes}`;
    } else {
      if (year === today.getFullYear()) {
        return `${month}-${day} ${hours}:${minutes}`;
      } else {
        return `${year}-${month}-${day} ${hours}:${minutes}`;
      }
    }
  };
</script>

<style>
  .container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #f5f7fa;
    padding-bottom: calc(56px + env(safe-area-inset-bottom));
  }

  .header {
    padding: 20px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #ffffff;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    position: sticky;
    top: 0;
    z-index: 10;
  }

  .title {
    font-size: 18px;
    font-weight: 600;
    color: #333;
  }

  .accordion-container {
    margin: 16px;
    padding-bottom: 10px;
  }

  .accordion-item {
    margin-bottom: 12px;
    border-radius: 8px;
    overflow: hidden;
    background-color: #ffffff;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  }

  .accordion-header {
    padding: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #ffffff;
    cursor: pointer;
  }

  .accordion-title {
    font-size: 16px;
    font-weight: 500;
    color: #333;
  }

  .accordion-icon {
    font-size: 14px;
    color: #4a86e8;
  }

  .accordion-content {
    background-color: #ffffff;
    padding: 0 16px 12px 16px;
    border-top: 1px solid #f0f0f0;
  }

  .empty-message {
    padding: 16px 0;
    text-align: center;
    color: #999;
    font-size: 14px;
  }

  .record-list {
    max-height: 300px;
    overflow-y: auto;
    padding-top: 12px;
  }

  .record-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #f5f5f5;
  }

  .record-item:last-child {
    border-bottom: none;
  }

  .record-info {
    flex: 1;
    margin-right: 8px;
  }

  .record-date {
    font-size: 12px;
    color: #666;
    margin-bottom: 4px;
    display: block;
  }

  .record-value {
    font-size: 15px;
    color: #333;
    word-break: break-word;
  }

  .record-actions {
    margin-left: auto;
  }

  .delete-btn {
    font-size: 13px;
    color: #ff4d4f;
    padding: 4px 8px;
    cursor: pointer;
  }

  .add-record-in-section {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 12px 0;
    margin-top: 10px;
    border-top: 1px dashed #eee;
    cursor: pointer;
    color: #4a86e8;
    font-size: 14px;
  }

  .add-icon {
    font-size: 20px;
    font-weight: bold;
    margin-right: 6px;
    line-height: 1;
  }

  /* Modal styles */
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal-content {
    width: 85%;
    max-width: 400px;
    max-height: 85vh;
    background-color: #fff;
    border-radius: 10px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  .modal-header {
    padding: 16px;
    border-bottom: 1px solid #f0f0f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .modal-title {
    font-size: 16px;
    font-weight: 600;
    color: #333;
  }

  .modal-close {
    font-size: 24px;
    color: #999;
    cursor: pointer;
  }

  .modal-body {
    padding: 16px;
    flex: 1;
    overflow-y: auto;
  }

  .modal-footer {
    padding: 12px 16px;
    border-top: 1px solid #f0f0f0;
    display: flex;
    justify-content: flex-end;
    background-color: #f9f9f9;
  }

  .cancel-btn {
    margin-right: 12px;
    padding: 8px 16px;
    background-color: #f5f5f5;
    color: #666;
    border-radius: 4px;
    font-size: 14px;
    border: 1px solid #ddd;
  }

  .confirm-btn {
    padding: 8px 16px;
    background-color: #4a86e8;
    color: white;
    border-radius: 4px;
    font-size: 14px;
    border: none;
  }

  /* Form styles */
  .form-item {
    margin-bottom: 16px;
  }

  .form-label {
    font-size: 14px;
    color: #666;
    margin-bottom: 8px;
    display: block;
  }

  .input,
  .textarea {
    box-sizing: border-box;
    width: 100%;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 0 12px;
    font-size: 14px;
    color: #333;
    background-color: #f9f9f9;
    height: 40px;
  }

  .textarea {
    height: 80px;
    padding: 8px 12px;
  }

  .picker {
    height: 40px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: #f9f9f9;
    display: flex;
    align-items: center;
    padding: 0 12px;
    box-sizing: border-box;
    width: 100%;
    position: relative;
  }

  .picker-value {
    font-size: 14px;
    color: #333;
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .picker::after {
    content: '▼';
    font-size: 12px;
    color: #999;
    margin-left: 8px;
  }

  .slider {
    margin: 15px 0;
  }

  /* Uni DateTime Picker styles */
  .uni-date {
    border: 1px solid #ddd !important;
    border-radius: 4px !important;
    background-color: #f9f9f9 !important;
    height: 40px !important;
    padding: 0 10px !important;
    box-sizing: border-box;
    display: flex !important;
    align-items: center !important;
  }

  .uni-date-editor--x .uni-date__input {
    background-color: transparent !important;
    color: #333 !important;
    font-size: 14px !important;
    height: 100% !important;
    line-height: normal !important;
    padding: 0 5px !important;
    margin: 0 !important;
    border: none !important;
    flex: 1;
  }

  .uni-date-editor--x .uni-date__input::-webkit-input-placeholder {
    color: #999 !important;
    font-size: 14px !important;
  }

  .uni-date-editor--x .uni-date__input:-ms-input-placeholder {
    color: #999 !important;
    font-size: 14px !important;
  }

  .uni-date-editor--x .uni-date__input::-moz-placeholder {
    color: #999 !important;
    font-size: 14px !important;
    opacity: 1;
  }

  .uni-date-editor--x .uni-date-header-icon,
  .uni-date-editor--x .uni-date__icon-clear {
    background-color: transparent !important;
    color: #909399 !important;
    padding: 0 5px !important;
    display: flex !important;
    align-items: center !important;
  }

  .uni-date-x--border {
    border: none !important;
  }

  .uni-date-editor--x {
    background-color: transparent !important;
  }

  .radio-group {
    width: 100%;
  }

  .radio-options {
    display: flex;
    width: 100%;
    border-radius: 4px;
    overflow: hidden;
  }

  .radio-option {
    flex: 1;
    text-align: center;
    background-color: #f5f5f5;
    padding: 10px 0;
    font-size: 14px;
    border: 1px solid #ddd;
    color: #666;
  }

  .radio-option:first-child {
    border-right: none;
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
  }

  .radio-option:last-child {
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
  }

  .radio-selected {
    background-color: #4a86e8;
    color: white;
    border-color: #4a86e8;
  }
</style>