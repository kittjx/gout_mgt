<template>
  <view class="accordion-item">
    <view class="accordion-header" @click="$emit('toggle', recordKey)">
      <text class="accordion-title">{{ title }}</text>
      <uni-icons class="accordion-icon" :type="isOpen ? 'bottom' : 'right'" size="16" color="var(--brand-color)"></uni-icons>
    </view>
    <uni-transition :show="isOpen" :duration="200" class="accordion-content-transition">
        <view class="accordion-content">
          <view v-if="!records || records.length === 0" class="empty-message">
            <uni-icons type="info" size="18" color="#999"></uni-icons>
            <text style="margin-left: 5px;">暂无记录，点击添加</text>
          </view>
          <view v-else class="record-list">
            <view v-for="(item, index) in records" :key="item.date.toISOString() + '-' + index" class="record-item">
              <view class="record-info">
                <text class="record-date">{{ formatDate(item.date) }}</text>
                <text class="record-value">{{ displayFormat(item) }}</text>
              </view>
              <view class="record-actions">
                 <button class="delete-btn mini-btn" size="mini" type="warn" plain @click.stop="$emit('delete', recordKey, index)">
                   <uni-icons type="trash" size="16" color="#e43d33"></uni-icons>
                   <text style="margin-left: 2px;">删除</text>
                 </button>
              </view>
            </view>
          </view>
          <button class="add-record-btn" type="primary" plain @click="$emit('add', recordKey)">
            <uni-icons type="plusempty" size="18" color="var(--brand-color)"></uni-icons>
            <text>添加{{ title }}</text>
          </button>
        </view>
    </uni-transition>
  </view>
</template>

<script setup>
import { formatDate } from '@/utils/formatters'; // Adjust path if necessary

// Props definition
const props = defineProps({
  title: { type: String, required: true },
  recordKey: { type: String, required: true },
  records: { type: Array, default: () => [] },
  isOpen: { type: Boolean, default: false },
  displayFormat: { type: Function, required: true } // Pass the formatting function from config
});

// Emits definition
defineEmits(['toggle', 'add', 'delete']);

</script>

<style scoped>
/* Scoped styles for RecordAccordionItem */
:root {
  --card-bg: #ffffff;
  --border-color: #f0f0f0;
  --text-color-primary: #333;
  --text-color-secondary: #666;
  --text-color-placeholder: #999;
  --brand-color: #2979ff; /* uni-app primary color */
  --danger-color: #e43d33; /* uni-app warn color */
  --base-padding: 16px;
  --border-radius: 8px;
}

.accordion-item {
  margin-bottom: 12px;
  border-radius: var(--border-radius);
  overflow: hidden; /* Needed for border-radius */
  background-color: var(--card-bg);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: margin 0.3s ease;
}

.accordion-header {
  padding: 12px var(--base-padding); /* Slightly reduced padding */
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  /* border-bottom: 1px solid var(--border-color); Add border only when open? */
  transition: background-color 0.2s ease;
}
.accordion-header:active {
    background-color: #f9f9f9;
}

.accordion-title {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-color-primary);
}

.accordion-icon {
  transition: transform 0.2s ease-out;
  margin-left: 8px;
}

/* Rotation handled by uni-icons type change */

.accordion-content-transition {
    /* Styles applied by uni-transition */
    will-change: height;
}

.accordion-content {
  background-color: var(--card-bg);
  padding: 0 var(--base-padding) var(--base-padding);
  border-top: 1px solid var(--border-color);
}

.empty-message {
  padding: 24px 0;
  display: flex;
  justify-content: center;
  align-items: center;
  color: var(--text-color-placeholder);
  font-size: 14px;
  text-align: center;
}

.record-list {
  /* max-height: 300px; Maybe remove fixed height, let it expand */
  overflow-y: auto; /* Still useful if content becomes very long */
  padding-top: 12px;
}

.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5; /* Lighter separator */
}

.record-item:last-child {
  border-bottom: none;
  padding-bottom: 0; /* No padding below last item before add button */
}

.record-info {
  flex: 1;
  margin-right: 10px; /* Increased spacing */
  overflow: hidden; /* Prevent long text from breaking layout */
}

.record-date {
  font-size: 12px;
  color: var(--text-color-secondary);
  margin-bottom: 4px;
  display: block; /* Ensure it takes its own line */
}

.record-value {
  font-size: 15px;
  color: var(--text-color-primary);
  word-wrap: break-word; /* Allow long values to wrap */
}

.record-actions {
  /* Actions aligned to the right */
  flex-shrink: 0; /* Prevent button from shrinking */
}

/* Mini button styling */
.mini-btn {
  padding: 2px 8px !important;
  font-size: 13px !important;
  line-height: 1.5 !important;
  display: inline-flex; /* Align icon and text */
  align-items: center;
}
/* Override uni-app plain button text color */
.delete-btn.button[plain] {
    color: var(--danger-color);
    border-color: var(--danger-color);
}
.delete-btn.button[plain]:active {
    background-color: rgba(228, 61, 51, 0.1); /* Light red background on press */
}

/* Add Record Button within section */
.add-record-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  margin-top: 16px;
  padding: 10px 0;
  font-size: 14px;
  /* Uses uni-app button styles (type="primary" plain) */
}
.add-record-btn[plain] {
    background-color: transparent !important; /* Ensure plain button is transparent */
    border-color: var(--brand-color);
    color: var(--brand-color);
}
.add-record-btn[plain]:active {
    background-color: rgba(41, 121, 255, 0.1); /* Light blue background on press */
}

.add-record-btn text {
    margin-left: 4px;
}

</style>
