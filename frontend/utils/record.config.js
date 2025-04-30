// utils/record.config.js
// Define structure for each record type
import { reactive } from 'vue';

export const recordConfigs = reactive({
  weight: {
    title: '体重记录',
    fields: [
      { label: '体重 (kg)', key: 'value', type: 'digit', placeholder: '请输入体重' }
    ],
    formatter: (item) => `${item.value}kg`,
    validator: (form) => form.value && !isNaN(parseFloat(form.value)),
    processor: (form, date) => ({ date, value: parseFloat(form.value) })
  },
  mainFood: {
    title: '主食记录',
    fields: [
      { label: '食物名称', key: 'name', type: 'text', placeholder: '请输入食物名称' },
      { label: '食用量', key: 'amount', type: 'text', placeholder: '例如: 1碗/100g' }
    ],
    formatter: (item) => `${item.name} - ${item.amount}`,
    validator: (form) => form.name && form.amount,
    processor: (form, date) => ({ date, name: form.name, amount: form.amount })
  },
  waterIntake: {
    title: '饮水量记录',
    fields: [
      { label: '饮水量 (ml)', key: 'amount', type: 'digit', placeholder: '请输入饮水量' }
    ],
    formatter: (item) => `${item.amount}ml`,
    validator: (form) => form.amount && !isNaN(parseInt(form.amount)),
    processor: (form, date) => ({ date, amount: parseInt(form.amount) })
  },
  purineFood: {
    title: '高嘌呤饮食',
    fields: [
      { label: '食物类型', key: 'type', type: 'text', placeholder: '例如: 海鲜/红肉' },
      { label: '食用量', key: 'amount', type: 'text', placeholder: '例如: 100g' }
    ],
    formatter: (item) => `${item.type} - ${item.amount}`,
    validator: (form) => form.type && form.amount,
    processor: (form, date) => ({ date, type: form.type, amount: form.amount })
  },
  uricAcid: {
    title: '尿酸监测',
    fields: [
      { label: '尿酸值 (μmol/L)', key: 'value', type: 'digit', placeholder: '请输入尿酸值' },
      { label: '检测方式', key: 'method', type: 'radio', placeholder: '请选择检测方式', options: ['医院检测', '自测'] }
    ],
    formatter: (item) => `${item.value}μmol/L (${item.method})`,
    validator: (form) => form.value && !isNaN(parseFloat(form.value)) && form.method,
    processor: (form, date) => ({ date, value: parseFloat(form.value), method: form.method })
  },
  urinePH: {
    title: '尿液酸碱值',
    fields: [
      { label: 'pH值', key: 'value', type: 'digit', placeholder: '请输入pH值' }
    ],
    formatter: (item) => `pH ${item.value}`,
    validator: (form) => form.value && !isNaN(parseFloat(form.value)),
    processor: (form, date) => ({ date, value: parseFloat(form.value) })
  },
  liverFunction: {
    title: '肝功能',
    fields: [
       { label: '检查结果', key: 'value', type: 'text', placeholder: '请输入肝功能结果', required: true }
    ],
    formatter: (item) => `${item.value}`,
    validator: (form) => form.value,
    processor: (form, date) => ({ date, value: form.value })
  },
  kidneyFunction: {
    title: '肾功能',
     fields: [
       { label: '检查结果', key: 'value', type: 'text', placeholder: '请输入肾功能结果', required: true }
    ],
    formatter: (item) => `${item.value}`,
    validator: (form) => form.value,
    processor: (form, date) => ({ date, value: form.value })
  },
  bloodSugar: {
    title: '血糖',
    fields: [
       { label: '血糖值 (mmol/L)', key: 'value', type: 'digit', placeholder: '请输入血糖值', required: true } // Specify unit
    ],
    formatter: (item) => `${item.value} mmol/L`,
    validator: (form) => form.value,
    processor: (form, date) => ({ date, value: form.value })
  },
  bloodPressure: {
    title: '血压',
    fields: [
       { label: '血压值 (mmHg)', key: 'value', type: 'text', placeholder: '例如: 120/80', required: true } // Specify unit hint
    ],
    formatter: (item) => `${item.value} mmHg`,
    validator: (form) => form.value,
    processor: (form, date) => ({ date, value: form.value })
  },
  bloodLipid: {
    title: '血脂',
    fields: [
       { label: '检查结果', key: 'value', type: 'text', placeholder: '请输入血脂结果', required: true } // Could be multiple fields
    ],
    formatter: (item) => `${item.value}`,
    validator: (form) => form.value,
    processor: (form, date) => ({ date, value: form.value })
  },
  attack: {
    title: '发作情况',
    fields: [
      { label: '持续时间 (小时)', key: 'duration', type: 'digit', placeholder: '请输入发作持续时间' },
      { label: '疼痛评分 (1-10)', key: 'painScore', type: 'slider', min: 1, max: 10 }
    ],
    formatter: (item) => `持续: ${item.duration}小时, 疼痛评分: ${item.painScore}/10`,
    validator: (form) => form.duration && !isNaN(parseFloat(form.duration)),
    processor: (form, date) => ({ date, duration: parseFloat(form.duration), painScore: parseInt(form.painScore) })
  },
  tophi: {
    title: '痛风石情况',
    fields: [
      { label: '部位', key: 'location', type: 'text', placeholder: '例如: 左脚大拇指' },
      { label: '直径 (mm)', key: 'diameter', type: 'digit', placeholder: '请输入直径' }
    ],
    formatter: (item) => `${item.location}: ${item.diameter}mm`,
    validator: (form) => form.location && form.diameter && !isNaN(parseFloat(form.diameter)),
    processor: (form, date) => ({ date, location: form.location, diameter: parseFloat(form.diameter) })
  },
  jointFunction: {
    title: '关节功能',
    fields: [
      { label: '关节', key: 'joint', type: 'text', placeholder: '例如: 左膝关节' },
      { label: '功能描述', key: 'description', type: 'textarea', placeholder: '请输入关节功能描述' }
    ],
    formatter: (item) => `${item.joint}: ${item.description}`,
    validator: (form) => form.joint && form.description,
    processor: (form, date) => ({ date, joint: form.joint, description: form.description })
  }
});

// Helper to initialize reactive state based on the config
export const initializeReactiveState = (initialData = {}) => {
  const openSections = {};
  const userRecords = {};

  recordConfigs.forEach(config => {
    // Default open state: only 'weight' or the first item if 'weight' doesn't exist
    openSections[config.key] = config.key === 'weight' || (recordConfigs.length > 0 && config.key === recordConfigs[0].key && !recordConfigs.some(c => c.key === 'weight'));
    // Initialize with provided data or empty array
    const records = initialData[config.key] || [];
    // Ensure dates are Date objects and sort
     if (records.length > 0) {
        userRecords[config.key] = records.map(record => ({
             ...record,
             date: record.date instanceof Date ? record.date : new Date(record.date) // Convert strings/timestamps to Date
         })).sort((a, b) => b.date.getTime() - a.date.getTime());
     } else {
        userRecords[config.key] = [];
     }
  });

  return {
    openSections: reactive(openSections),
    userRecords: reactive(userRecords)
  };
};