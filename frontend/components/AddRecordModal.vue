<template>
  <uni-popup ref="popupRef" type="center" :is-mask-click="true" @maskClick="closeModal">
    <view class="modal-content-wrapper">
      <view class="modal-header">
        <text class="modal-title">新增 {{ config?.title || '记录' }}</text>
         <uni-icons class="modal-close" type="close" size="24" color="#999" @click="closeModal"></uni-icons>
      </view>

      <scroll-view scroll-y class="modal-body">
        <view class="form-item">
          <text class="form-label">记录时间</text>
          <uni-datetime-picker
            ref="dateTimePickerRef"
            type="datetime"
            v-model="selectedDateTime"
            :start="dateRange.start"
            :end="dateRange.end"
            return-type="string"
            placeholder="请选择记录时间"
            class="datetime-picker-input"
          />
        </view>

        <view v-if="config && config.modalFields">
            <view v-for="field in config.modalFields" :key="field.name" class="form-item">
              <text class="form-label">
                  {{ field.label }}
                  <text v-if="field.required" class="required-star">*</text>
              </text>

              <input
                v-if="field.type === 'text' || field.type === 'digit'"
                :type="field.type"
                v-model="formData[field.name]"
                :placeholder="field.placeholder"
                placeholder-class="input-placeholder"
                class="input"
              />

              <textarea
                v-if="field.type === 'textarea'"
                v-model="formData[field.name]"
                :placeholder="field.placeholder"
                placeholder-class="input-placeholder"
                class="textarea"
                auto-height
                maxlength="-1"
              />

              <picker
                v-if="field.type === 'picker'"
                :range="field.options"
                @change="onPickerChange($event, field.name)"
                class="picker"
              >
                 <view class="picker-value" :class="{ 'placeholder': !formData[field.name] }">
                    {{ formData[field.name] || field.placeholder }}
                </view>
              </picker>

              <view v-if="field.type === 'slider'" class="slider-container">
                 <slider
                   v-model="formData[field.name]"
                   :min="field.min"
                   :max="field.max"
                   show-value
                   :active-color="brandColor"
                   class="slider"
                 />
              </view>
            </view>
        </view>
        <view v-else class="loading-placeholder">
            <text>加载中...</text>
        </view>

      </scroll-view>

      <view class="modal-footer">
        <button class="form-btn cancel-btn" @click="closeModal">取消</button>
        <button class="form-btn confirm-btn" type="primary" @click="saveRecord">确认添加</button>
      </view>
    </view>
  </uni-popup>
</template>

<script setup>
import { ref, reactive, watch, nextTick } from 'vue';
import { getCurrentFormattedDateTimeString } from '@/utils/formatters'; // Adjust path

// Component Refs
const popupRef = ref(null);
const dateTimePickerRef = ref(null); // Ref for the picker if needed

// Props and Emits
const props = defineProps({
  isVisible: { type: Boolean, default: false }, // Used to control opening
  config: { type: Object, default: null } // Pass the specific config for the type
});
const emit = defineEmits(['update:isVisible', 'save']);

// Reactive State
const formData = reactive({});
const selectedDateTime = ref('');
const dateRange = reactive({ start: '2020-01-01 00:00:00', end: '2030-12-31 23:59:59' });
const brandColor = ref('#2979ff'); // Store brand color for slider

// Watcher to open/close popup based on isVisible prop
watch(() => props.isVisible, (newValue) => {
  if (newValue) {
    initializeForm(); // Initialize form when opening
    popupRef.value?.open();
  } else {
    popupRef.value?.close();
  }
});

// Watcher to reset form when config changes (might happen if modal stays open and type changes - less likely now)
watch(() => props.config, (newConfig) => {
  if (newConfig) {
     initializeForm();
  }
}, { deep: true }); // Use deep watch if config structure is complex and might change internally

// --- Methods ---

// Initialize or reset the form based on the current config
const initializeForm = () => {
    selectedDateTime.value = getCurrentFormattedDateTimeString();

    if (props.config && props.config.modalFields) {
        // Clear previous formData keys to avoid stale data
        Object.keys(formData).forEach(key => delete formData[key]);

        // Set initial values from config
        props.config.modalFields.forEach(field => {
            formData[field.name] = field.initial !== undefined ? field.initial : (field.type === 'slider' ? (field.min || 0) : '');
        });
    } else {
        // Clear form data if config is invalid
        Object.keys(formData).forEach(key => delete formData[key]);
    }
};

// Handle picker changes
const onPickerChange = (e, fieldName) => {
  const fieldConfig = props.config?.modalFields?.find(f => f.name === fieldName);
  if (fieldConfig && e.detail.value !== null && e.detail.value !== undefined) {
    formData[fieldName] = fieldConfig.options[e.detail.value];
  }
};

// Close modal logic
const closeModal = () => {
  // Let uni-popup handle closing animation, just update the prop
  emit('update:isVisible', false);
};

// Save record logic
const saveRecord = () => {
  // 1. Basic Config Check
   if (!props.config || !props.config.modalFields) {
       uni.showToast({ title: '配置错误', icon: 'none' });
       console.error("Modal config is missing or invalid.");
       return;
   }

  // 2. Validate DateTime
  if (!selectedDateTime.value) {
    uni.showToast({ title: '请选择记录时间', icon: 'none' });
    return;
  }
  const recordDate = new Date(selectedDateTime.value.replace(/-/g, "/")); // Basic parsing
  if (isNaN(recordDate.getTime())) {
    uni.showToast({ title: '无效的日期时间格式', icon: 'none' });
    console.error("Invalid date constructed from picker:", selectedDateTime.value);
    return;
  }

  // 3. Validate Form Fields based on config
  for (const field of props.config.modalFields) {
      const value = formData[field.name];
      // Check required fields
      if (field.required && (value === '' || value === null || value === undefined)) {
           uni.showToast({ title: `请填写${field.label}`, icon: 'none' });
           return; // Stop validation
      }
      // Add specific type validation if needed (e.g., for digit fields)
      if (field.type === 'digit' && value !== '' && isNaN(parseFloat(value))) {
           uni.showToast({ title: `${field.label}必须是有效的数字`, icon: 'none' });
           return; // Stop validation
      }
      // Add more validation rules here (e.g., regex for blood pressure)
  }

  // 4. Prepare data to emit (create a clean copy)
   const recordData = {};
   for (const field of props.config.modalFields) {
       let value = formData[field.name];
        // Convert numeric strings for digit fields before emitting
        if (field.type === 'digit' && typeof value === 'string' && value !== '') {
            value = parseFloat(value);
        } else if (field.type === 'slider' && typeof value !== 'number') {
            // Ensure slider value is a number
             value = parseInt(value, 10) || field.min || 0;
        }
       recordData[field.name] = value;
   }


  // 5. Emit Save Event
  emit('save', {
    recordKey: props.config.key,
    date: recordDate,
    data: recordData
  });

  // 6. Close Modal (via v-model binding)
  closeModal();
};

</script>

<style scoped>
/* Scoped styles for AddRecordModal */
:root {
  /* Re-define variables if needed locally or rely on global ones */
  --modal-bg: #ffffff;
  --modal-border-radius: 10px;
  --form-padding: 16px;
  --input-bg: #f7f7f7; /* Slightly different bg for inputs */
  --input-border-color: #e5e5e5;
  --input-height: 40px;
  --input-radius: 6px;
  --text-color-primary: #333;
  --text-color-secondary: #666;
  --text-color-placeholder: #ababab; /* Lighter placeholder */
  --brand-color: #2979ff;
  --danger-color: #e43d33;
}

/* Override uni-popup background if needed */
.uni-popup {
    z-index: 999; /* Ensure it's above other content */
}

.modal-content-wrapper {
  width: 88vw; /* Use viewport width */
  max-width: 450px; /* Max width on larger screens */
  background-color: var(--modal-bg);
  border-radius: var(--modal-border-radius);
  overflow: hidden; /* Clip content */
  display: flex;
  flex-direction: column;
  /* max-height: 85vh; Height managed by scroll-view */
}

.modal-header {
  padding: 12px var(--form-padding);
  border-bottom: 1px solid var(--input-border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative; /* For absolute positioning of close button if needed */
  background-color: #f9f9f9; /* Slight header background */
}

.modal-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color-primary);
  text-align: center;
  flex-grow: 1; /* Allow title to take space */
}

.modal-close {
  position: absolute;
  right: var(--form-padding);
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
}

/* Scrollable body */
.modal-body {
  padding: var(--form-padding);
  flex: 1; /* Allow body to take remaining space */
  max-height: 65vh; /* Limit body height to prevent overflow */
  overflow-y: auto; /* Enable vertical scroll */
  box-sizing: border-box;
}

.loading-placeholder {
    text-align: center;
    padding: 30px;
    color: var(--text-color-secondary);
}

.modal-footer {
  padding: 12px var(--form-padding);
  border-top: 1px solid var(--input-border-color);
  display: flex;
  justify-content: space-between; /* Space out buttons */
  background-color: #f9f9f9;
}

/* Form Styles */
.form-item {
  margin-bottom: 18px; /* Increased spacing */
}
.form-item:last-child {
    margin-bottom: 0; /* No margin for last item */
}

.form-label {
  font-size: 14px;
  color: var(--text-color-secondary);
  margin-bottom: 8px;
  display: block; /* Take full width */
}
.required-star {
    color: var(--danger-color);
    margin-left: 4px;
    font-weight: bold;
}


/* Input, Textarea common styles */
.input, .textarea {
  box-sizing: border-box;
  width: 100%;
  border: 1px solid var(--input-border-color);
  border-radius: var(--input-radius);
  padding: 0 12px;
  font-size: 14px;
  color: var(--text-color-primary);
  background-color: var(--input-bg);
  height: var(--input-height);
  line-height: normal; /* Reset line height */
}
.input:focus, .textarea:focus {
    border-color: var(--brand-color);
    background-color: #fff; /* White background on focus */
}

/* Placeholder style */
.input-placeholder {
  color: var(--text-color-placeholder);
  font-size: 14px;
}

/* Textarea specific styles */
.textarea {
  height: auto; /* Let auto-height work */
  min-height: 80px; /* Minimum height */
  padding: 8px 12px; /* Vertical padding */
  line-height: 1.5; /* Better line spacing */
}

/* Picker specific styles */
.picker {
  height: var(--input-height);
  border: 1px solid var(--input-border-color);
  border-radius: var(--input-radius);
  background-color: var(--input-bg);
  display: flex;
  align-items: center;
  padding: 0 12px;
  box-sizing: border-box;
  width: 100%;
  position: relative; /* Needed for pseudo-element */
  justify-content: space-between; /* Space text and arrow */
}

.picker-value {
  font-size: 14px;
  color: var(--text-color-primary);
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-right: 8px; /* Space before arrow */
}
.picker-value.placeholder {
    color: var(--text-color-placeholder); /* Style placeholder */
}

.picker::after {
    content: ''; /* Using uni-icons now */
    display: none; /* Hide default pseudo arrow */
}
/* Add uni-icon for picker dropdown arrow */
.picker::before {
    font-family: uniicons;
    content: '\e6bc'; /* uni-icons arrow down code */
    font-size: 16px;
    color: var(--text-color-secondary);
}


/* Slider specific styles */
.slider-container {
    padding-top: 10px; /* Add some space above slider */
}
.slider {
   margin: 0; /* Remove default margins if any */
   width: 100%;
}

/* Datetime Picker Styles (overrides, place in global if needed) */
.datetime-picker-input {
    /* Reuse input styles */
    box-sizing: border-box;
    width: 100%;
    border: 1px solid var(--input-border-color);
    border-radius: var(--input-radius);
    padding: 0 12px;
    font-size: 14px;
    color: var(--text-color-primary);
    background-color: var(--input-bg);
    height: var(--input-height);
    display: flex; /* Use flex for alignment */
    align-items: center;
}
/* Ensure inner text looks right */
:deep(.datetime-picker-input .uni-date__x-input) {
    font-size: 14px !important;
    color: var(--text-color-primary) !important;
    background-color: transparent !important;
}
/* Placeholder color */
:deep(.datetime-picker-input .uni-date__x-input::placeholder) {
    color: var(--text-color-placeholder) !important;
}
:deep(.datetime-picker-input .uni-date__icon-clear),
:deep(.datetime-picker-input .uni-date-header-icon) {
    color: var(--text-color-secondary) !important;
}


/* Footer Button Styles */
.form-btn {
    flex: 1; /* Make buttons take equal space */
    margin: 0 6px; /* Add spacing between buttons */
    font-size: 15px;
    padding: 10px 0;
    line-height: normal; /* Reset button line-height */
}
.form-btn:first-child {
    margin-left: 0;
}
.form-btn:last-child {
    margin-right: 0;
}

.cancel-btn {
    background-color: #f5f5f5;
    color: #666;
    border: 1px solid #ddd;
    /* uni-app button reset */
    border-radius: var(--input-radius);
    padding: 0; /* Reset uni-app padding */
    height: 38px;
    line-height: 38px;
}
.cancel-btn::after {
    border: none; /* Remove uni-app button border */
}
.cancel-btn:active {
    background-color: #eee;
}

.confirm-btn {
     /* Uses uni-app primary styles */
     border-radius: var(--input-radius);
     height: 38px;
     line-height: 38px;
}

</style>