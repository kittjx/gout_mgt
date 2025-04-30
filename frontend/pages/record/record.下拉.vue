<template>
  <view class="record-page">

    
    <view class="record-types">
      <view class="type-selector">
        <text>选择记录类型：</text>
        <picker :value="selectedTypeIndex" :range="recordTypes" @change="handleTypeChange">
          <view class="picker-value">
            {{ recordTypes[selectedTypeIndex] }}
            <text class="icon">▼</text>
          </view>
        </picker>
      </view>
      
      <button class="add-btn" @click="showAddForm = true">添加记录</button>
    </view>
    
    <!-- 体重记录表单 -->
    <view class="add-form" v-if="showAddForm && selectedTypeIndex === 0">
      <view class="form-header">
        <text>添加体重记录</text>
        <text class="close-btn" @click="showAddForm = false">×</text>
      </view>
      <view class="form-item">
        <text class="label">记录时间</text>
        <picker mode="date" :value="formData.weight.date" @change="(e) => formData.weight.date = e.detail.value">
          <view class="picker-value">{{ formData.weight.date }}</view>
        </picker>
      </view>
      <view class="form-item">
        <text class="label">体重(kg)</text>
        <input type="digit" v-model="formData.weight.value" placeholder="请输入体重" />
      </view>
      <button class="submit-btn" @click="addWeightRecord">保存</button>
    </view>
    
    <!-- 主食记录表单 -->
    <view class="add-form" v-if="showAddForm && selectedTypeIndex === 1">
      <view class="form-header">
        <text>添加主食记录</text>
        <text class="close-btn" @click="showAddForm = false">×</text>
      </view>
      <view class="form-item">
        <text class="label">记录时间</text>
        <picker mode="date" :value="formData.food.date" @change="(e) => formData.food.date = e.detail.value">
          <view class="picker-value">{{ formData.food.date }}</view>
        </picker>
      </view>
      <view class="form-item">
        <text class="label">主食类型</text>
        <input type="text" v-model="formData.food.type" placeholder="例如：米饭、面条" />
      </view>
      <view class="form-item">
        <text class="label">数量(克)</text>
        <input type="digit" v-model="formData.food.amount" placeholder="请输入数量" />
      </view>
      <button class="submit-btn" @click="addFoodRecord">保存</button>
    </view>
    
    <!-- 饮水量记录表单 -->
    <view class="add-form" v-if="showAddForm && selectedTypeIndex === 2">
      <view class="form-header">
        <text>添加饮水量记录</text>
        <text class="close-btn" @click="showAddForm = false">×</text>
      </view>
      <view class="form-item">
        <text class="label">记录时间</text>
        <picker mode="date" :value="formData.water.date" @change="(e) => formData.water.date = e.detail.value">
          <view class="picker-value">{{ formData.water.date }}</view>
        </picker>
      </view>
      <view class="form-item">
        <text class="label">饮水量(ml)</text>
        <input type="digit" v-model="formData.water.amount" placeholder="请输入饮水量" />
      </view>
      <button class="submit-btn" @click="addWaterRecord">保存</button>
    </view>
    
    <!-- 高嘌呤饮食记录表单 -->
    <view class="add-form" v-if="showAddForm && selectedTypeIndex === 3">
      <view class="form-header">
        <text>添加高嘌呤饮食记录</text>
        <text class="close-btn" @click="showAddForm = false">×</text>
      </view>
      <view class="form-item">
        <text class="label">记录时间</text>
        <picker mode="date" :value="formData.purine.date" @change="(e) => formData.purine.date = e.detail.value">
          <view class="picker-value">{{ formData.purine.date }}</view>
        </picker>
      </view>
      <view class="form-item">
        <text class="label">食物种类</text>
        <input type="text" v-model="formData.purine.type" placeholder="例如：海鲜、动物内脏" />
      </view>
      <view class="form-item">
        <text class="label">数量(克)</text>
        <input type="digit" v-model="formData.purine.amount" placeholder="请输入数量" />
      </view>
      <button class="submit-btn" @click="addPurineRecord">保存</button>
    </view>
    
    <!-- 尿酸监测记录表单 -->
    <view class="add-form" v-if="showAddForm && selectedTypeIndex === 4">
      <view class="form-header">
        <text>添加尿酸监测记录</text>
        <text class="close-btn" @click="showAddForm = false">×</text>
      </view>
      <view class="form-item">
        <text class="label">记录时间</text>
        <picker mode="date" :value="formData.uricAcid.date" @change="(e) => formData.uricAcid.date = e.detail.value">
          <view class="picker-value">{{ formData.uricAcid.date }}</view>
        </picker>
      </view>
      <view class="form-item">
        <text class="label">尿酸值(μmol/L)</text>
        <input type="digit" v-model="formData.uricAcid.value" placeholder="请输入尿酸值" />
      </view>
      <view class="form-item">
        <text class="label">采集方式</text>
        <picker :value="formData.uricAcid.methodIndex" :range="collectMethods" @change="(e) => formData.uricAcid.methodIndex = e.detail.value">
          <view class="picker-value">{{ collectMethods[formData.uricAcid.methodIndex] }}</view>
        </picker>
      </view>
      <button class="submit-btn" @click="addUricAcidRecord">保存</button>
    </view>
    
    <!-- 其他记录表单 -->
    <view class="add-form" v-if="showAddForm && selectedTypeIndex === 5">
      <view class="form-header">
        <text>添加尿液酸碱值记录</text>
        <text class="close-btn" @click="showAddForm = false">×</text>
      </view>
      <view class="form-item">
        <text class="label">记录时间</text>
        <picker mode="date" :value="formData.urinePH.date" @change="(e) => formData.urinePH.date = e.detail.value">
          <view class="picker-value">{{ formData.urinePH.date }}</view>
        </picker>
      </view>
      <view class="form-item">
        <text class="label">pH值</text>
        <input type="digit" v-model="formData.urinePH.value" placeholder="请输入pH值" />
      </view>
      <button class="submit-btn" @click="addUrinePHRecord">保存</button>
    </view>
    
    <!-- 发作情况记录表单 -->
    <view class="add-form" v-if="showAddForm && selectedTypeIndex === 6">
      <view class="form-header">
        <text>添加发作情况记录</text>
        <text class="close-btn" @click="showAddForm = false">×</text>
      </view>
      <view class="form-item">
        <text class="label">发作时间</text>
        <picker mode="date" :value="formData.attack.date" @change="(e) => formData.attack.date = e.detail.value">
          <view class="picker-value">{{ formData.attack.date }}</view>
        </picker>
      </view>
      <view class="form-item">
        <text class="label">持续时间(小时)</text>
        <input type="digit" v-model="formData.attack.duration" placeholder="请输入持续时间" />
      </view>
      <view class="form-item">
        <text class="label">疼痛评分(1-10)</text>
        <slider 
          min="1" 
          max="10" 
          step="1" 
          :value="formData.attack.painScore" 
          show-value 
          @change="(e) => formData.attack.painScore = e.detail.value"
        />
      </view>
      <button class="submit-btn" @click="addAttackRecord">保存</button>
    </view>
    
    <!-- 痛风石记录表单 -->
    <view class="add-form" v-if="showAddForm && selectedTypeIndex === 7">
      <view class="form-header">
        <text>添加痛风石记录</text>
        <text class="close-btn" @click="showAddForm = false">×</text>
      </view>
      <view class="form-item">
        <text class="label">记录时间</text>
        <picker mode="date" :value="formData.tophus.date" @change="(e) => formData.tophus.date = e.detail.value">
          <view class="picker-value">{{ formData.tophus.date }}</view>
        </picker>
      </view>
      <view class="form-item">
        <text class="label">痛风石直径(mm)</text>
        <input type="digit" v-model="formData.tophus.diameter" placeholder="请输入直径" />
      </view>
      <view class="form-item">
        <text class="label">位置</text>
        <input type="text" v-model="formData.tophus.location" placeholder="请输入位置" />
      </view>
      <button class="submit-btn" @click="addTophusRecord">保存</button>
    </view>
    
    <!-- 关节功能记录表单 -->
    <view class="add-form" v-if="showAddForm && selectedTypeIndex === 8">
      <view class="form-header">
        <text>添加关节功能记录</text>
        <text class="close-btn" @click="showAddForm = false">×</text>
      </view>
      <view class="form-item">
        <text class="label">记录时间</text>
        <picker mode="date" :value="formData.joint.date" @change="(e) => formData.joint.date = e.detail.value">
          <view class="picker-value">{{ formData.joint.date }}</view>
        </picker>
      </view>
      <view class="form-item">
        <text class="label">关节部位</text>
        <input type="text" v-model="formData.joint.location" placeholder="请输入关节部位" />
      </view>
      <view class="form-item">
        <text class="label">活动度(%)</text>
        <slider 
          min="0" 
          max="100" 
          step="5" 
          :value="formData.joint.mobility" 
          show-value 
          @change="(e) => formData.joint.mobility = e.detail.value"
        />
      </view>
      <button class="submit-btn" @click="addJointRecord">保存</button>
    </view>
    
    <!-- 记录列表 -->
    <view class="record-list">
      <view class="list-header">
        <text>{{ recordTypes[selectedTypeIndex] }}记录列表</text>
      </view>
      
      <!-- 体重记录列表 -->
      <view class="list-content" v-if="selectedTypeIndex === 0">
        <view class="empty-tip" v-if="records.weight.length === 0">
          <text>暂无记录</text>
        </view>
        <view class="record-item" v-for="(item, index) in records.weight" :key="index">
          <view class="record-info">
            <text class="record-date">{{ item.date }}</text>
            <text class="record-value">{{ item.value }}kg</text>
          </view>
          <text class="delete-btn" @click="deleteRecord('weight', index)">删除</text>
        </view>
      </view>
      
      <!-- 主食记录列表 -->
      <view class="list-content" v-if="selectedTypeIndex === 1">
        <view class="empty-tip" v-if="records.food.length === 0">
          <text>暂无记录</text>
        </view>
        <view class="record-item" v-for="(item, index) in records.food" :key="index">
          <view class="record-info">
            <text class="record-date">{{ item.date }}</text>
            <text class="record-value">{{ item.type }} {{ item.amount }}克</text>
          </view>
          <text class="delete-btn" @click="deleteRecord('food', index)">删除</text>
        </view>
      </view>
      
      <!-- 饮水量记录列表 -->
      <view class="list-content" v-if="selectedTypeIndex === 2">
        <view class="empty-tip" v-if="records.water.length === 0">
          <text>暂无记录</text>
        </view>
        <view class="record-item" v-for="(item, index) in records.water" :key="index">
          <view class="record-info">
            <text class="record-date">{{ item.date }}</text>
            <text class="record-value">{{ item.amount }}ml</text>
          </view>
          <text class="delete-btn" @click="deleteRecord('water', index)">删除</text>
        </view>
      </view>
      
      <!-- 高嘌呤饮食记录列表 -->
      <view class="list-content" v-if="selectedTypeIndex === 3">
        <view class="empty-tip" v-if="records.purine.length === 0">
          <text>暂无记录</text>
        </view>
        <view class="record-item" v-for="(item, index) in records.purine" :key="index">
          <view class="record-info">
            <text class="record-date">{{ item.date }}</text>
            <text class="record-value">{{ item.type }} {{ item.amount }}克</text>
          </view>
          <text class="delete-btn" @click="deleteRecord('purine', index)">删除</text>
        </view>
      </view>
      
      <!-- 尿酸监测记录列表 -->
      <view class="list-content" v-if="selectedTypeIndex === 4">
        <view class="empty-tip" v-if="records.uricAcid.length === 0">
          <text>暂无记录</text>
        </view>
        <view class="record-item" v-for="(item, index) in records.uricAcid" :key="index">
          <view class="record-info">
            <text class="record-date">{{ item.date }}</text>
            <text class="record-value">{{ item.value }}μmol/L ({{ item.method }})</text>
          </view>
          <text class="delete-btn" @click="deleteRecord('uricAcid', index)">删除</text>
        </view>
      </view>
      
      <!-- 尿液酸碱值记录列表 -->
      <view class="list-content" v-if="selectedTypeIndex === 5">
        <view class="empty-tip" v-if="records.urinePH.length === 0">
          <text>暂无记录</text>
        </view>
        <view class="record-item" v-for="(item, index) in records.urinePH" :key="index">
          <view class="record-info">
            <text class="record-date">{{ item.date }}</text>
            <text class="record-value">pH: {{ item.value }}</text>
          </view>
          <text class="delete-btn" @click="deleteRecord('urinePH', index)">删除</text>
        </view>
      </view>
      
      <!-- 发作情况记录列表 -->
      <view class="list-content" v-if="selectedTypeIndex === 6">
        <view class="empty-tip" v-if="records.attack.length === 0">
          <text>暂无记录</text>
        </view>
        <view class="record-item" v-for="(item, index) in records.attack" :key="index">
          <view class="record-info">
            <text class="record-date">{{ item.date }}</text>
            <text class="record-value">持续{{ item.duration }}小时，疼痛评分: {{ item.painScore }}</text>
          </view>
          <text class="delete-btn" @click="deleteRecord('attack', index)">删除</text>
        </view>
      </view>
      
      <!-- 痛风石记录列表 -->
      <view class="list-content" v-if="selectedTypeIndex === 7">
        <view class="empty-tip" v-if="records.tophus.length === 0">
          <text>暂无记录</text>
        </view>
        <view class="record-item" v-for="(item, index) in records.tophus" :key="index">
          <view class="record-info">
            <text class="record-date">{{ item.date }}</text>
            <text class="record-value">{{ item.location }}：{{ item.diameter }}mm</text>
          </view>
          <text class="delete-btn" @click="deleteRecord('tophus', index)">删除</text>
        </view>
      </view>
      
      <!-- 关节功能记录列表 -->
      <view class="list-content" v-if="selectedTypeIndex === 8">
        <view class="empty-tip" v-if="records.joint.length === 0">
          <text>暂无记录</text>
        </view>
        <view class="record-item" v-for="(item, index) in records.joint" :key="index">
          <view class="record-info">
            <text class="record-date">{{ item.date }}</text>
            <text class="record-value">{{ item.location }}：活动度{{ item.mobility }}%</text>
          </view>
          <text class="delete-btn" @click="deleteRecord('joint', index)">删除</text>
        </view>
      </view>
    </view>
    
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue';

// 记录类型列表
const recordTypes = [
  '体重',
  '主食',
  '饮水量',
  '高嘌呤饮食',
  '尿酸监测',
  '尿液酸碱值',
  '发作情况',
  '痛风石',
  '关节功能'
];

// 采集方式选项
const collectMethods = ['血液检测', '便携式设备', '医院检查'];

// 当前选中的记录类型索引
const selectedTypeIndex = ref(0);

// 是否显示添加表单
const showAddForm = ref(false);

// 表单数据
const formData = reactive({
  weight: {
    date: new Date().toISOString().split('T')[0],
    value: ''
  },
  food: {
    date: new Date().toISOString().split('T')[0],
    type: '',
    amount: ''
  },
  water: {
    date: new Date().toISOString().split('T')[0],
    amount: ''
  },
  purine: {
    date: new Date().toISOString().split('T')[0],
    type: '',
    amount: ''
  },
  uricAcid: {
    date: new Date().toISOString().split('T')[0],
    value: '',
    methodIndex: 0
  },
  urinePH: {
    date: new Date().toISOString().split('T')[0],
    value: ''
  },
  attack: {
    date: new Date().toISOString().split('T')[0],
    duration: '',
    painScore: 5
  },
  tophus: {
    date: new Date().toISOString().split('T')[0],
    diameter: '',
    location: ''
  },
  joint: {
    date: new Date().toISOString().split('T')[0],
    location: '',
    mobility: 50
  }
});

// 记录数据
const records = reactive({
  weight: [],
  food: [],
  water: [],
  purine: [],
  uricAcid: [],
  urinePH: [],
  attack: [],
  tophus: [],
  joint: []
});

// 初始化一些模拟数据
records.weight.push({ date: '2025-04-15', value: 75.5 });
records.weight.push({ date: '2025-04-10', value: 76.2 });
records.uricAcid.push({ date: '2025-04-05', value: 428, method: '血液检测' });
records.attack.push({ date: '2025-03-28', duration: 6, painScore: 8 });

// 切换记录类型
const handleTypeChange = (e) => {
  selectedTypeIndex.value = e.detail.value;
};

// 添加体重记录
const addWeightRecord = () => {
  if (!formData.weight.value) {
    uni.showToast({ title: '请输入体重', icon: 'none' });
    return;
  }
  
  records.weight.unshift({
    date: formData.weight.date,
    value: parseFloat(formData.weight.value)
  });
  
  // 重置表单并关闭
  formData.weight.value = '';
  showAddForm.value = false;
  
  uni.showToast({ title: '添加成功' });
};

// 添加主食记录
const addFoodRecord = () => {
  if (!formData.food.type || !formData.food.amount) {
    uni.showToast({ title: '请填写完整信息', icon: 'none' });
    return;
  }
  
  records.food.unshift({
    date: formData.food.date,
    type: formData.food.type,
    amount: parseFloat(formData.food.amount)
  });
  
  // 重置表单并关闭
  formData.food.type = '';
  formData.food.amount = '';
  showAddForm.value = false;
  
  uni.showToast({ title: '添加成功' });
};

// 添加饮水量记录
const addWaterRecord = () => {
  if (!formData.water.amount) {
    uni.showToast({ title: '请输入饮水量', icon: 'none' });
    return;
  }
  
  records.water.unshift({
    date: formData.water.date,
    amount: parseFloat(formData.water.amount)
  });
  
  // 重置表单并关闭
  formData.water.amount = '';
  showAddForm.value = false;
  
  uni.showToast({ title: '添加成功' });
};

// 添加高嘌呤饮食记录
const addPurineRecord = () => {
  if (!formData.purine.type || !formData.purine.amount) {
    uni.showToast({ title: '请填写完整信息', icon: 'none' });
    return;
  }
  
  records.purine.unshift({
    date: formData.purine.date,
    type: formData.purine.type,
    amount: parseFloat(formData.purine.amount)
  });
  
  // 重置表单并关闭
  formData.purine.type = '';
  formData.purine.amount = '';
  showAddForm.value = false;
  
  uni.showToast({ title: '添加成功' });
};

// 添加尿酸监测记录
const addUricAcidRecord = () => {
  if (!formData.uricAcid.value) {
    uni.showToast({ title: '请输入尿酸值', icon: 'none' });
    return;
  }
  
  records.uricAcid.unshift({
    date: formData.uricAcid.date,
    value: parseFloat(formData.uricAcid.value),
    method: collectMethods[formData.uricAcid.methodIndex]
  });
  
  // 重置表单并关闭
  formData.uricAcid.value = '';
  showAddForm.value = false;
  
  uni.showToast({ title: '添加成功' });
};

// 添加尿液酸碱值记录
const addUrinePHRecord = () => {
  if (!formData.urinePH.value) {
    uni.showToast({ title: '请输入pH值', icon: 'none' });
    return;
  }
  
  records.urinePH.unshift({
    date: formData.urinePH.date,
    value: parseFloat(formData.urinePH.value)
  });
  
  // 重置表单并关闭
  formData.urinePH.value = '';
  showAddForm.value = false;
  
  uni.showToast({ title: '添加成功' });
};

// 添加发作情况记录
const addAttackRecord = () => {
  if (!formData.attack.duration) {
    uni.showToast({ title: '请输入持续时间', icon: 'none' });
    return;
  }
  
  records.attack.unshift({
    date: formData.attack.date,
    duration: parseFloat(formData.attack.duration),
    painScore: formData.attack.painScore
  });
  
  // 重置表单并关闭
  formData.attack.duration = '';
  formData.attack.painScore = 5;
  showAddForm.value = false;
  
  uni.showToast({ title: '添加成功' });
};

// 添加痛风石记录
const addTophusRecord = () => {
  if (!formData.tophus.diameter || !formData.tophus.location) {
    uni.showToast({ title: '请填写完整信息', icon: 'none' });
    return;
  }
  
  records.tophus.unshift({
    date: formData.tophus.date,
    diameter: parseFloat(formData.tophus.diameter),
    location: formData.tophus.location
  });
  
  // 重置表单并关闭
  formData.tophus.diameter = '';
  formData.tophus.location = '';
  showAddForm.value = false;
  
  uni.showToast({ title: '添加成功' });
};

// 添加关节功能记录
const addJointRecord = () => {
  if (!formData.joint.location) {
    uni.showToast({ title: '请输入关节部位', icon: 'none' });
    return;
  }
  
  records.joint.unshift({
    date: formData.joint.date,
    location: formData.joint.location,
    mobility: formData.joint.mobility
  });
  
  // 重置表单并关闭
  formData.joint.location = '';
  formData.joint.mobility = 50;
  showAddForm.value = false;
  
  uni.showToast({ title: '添加成功' });
};

// 删除记录
const deleteRecord = (type, index) => {
  uni.showModal({
    title: '确认删除',
    content: '是否确认删除该条记录？',
    success: (res) => {
      if (res.confirm) {
        records[type].splice(index, 1);
        uni.showToast({ title: '删除成功' });
      }
    }
  });
};

// 页面导航
const navigateTo = (url) => {
  uni.navigateTo({ url });
};
</script>

<style>
.record-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8f9fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.header {
  background-color: #007aff;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.title {
  color: #ffffff;
  font-size: 22px;
  font-weight: 600;
}

.record-types {
  padding: 15px;
  background-color: #ffffff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.type-selector {
  display: flex;
  align-items: center;
}

.picker-value {
  background-color: #f1f5f9;
  padding: 8px 12px;
  border-radius: 6px;
  min-width: 120px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.icon {
  font-size: 12px;
  color: #64748b;
  margin-left: 5px;
}

.add-btn {
  background-color: #007aff;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  padding: 8px 15px;
  font-size: 14px;
}

.add-form {
  margin: 0 15px 15px;
  background-color: #ffffff;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e2e8f0;
  font-weight: 600;
}

.close-btn {
  font-size: 20px;
  color: #64748b;
}

.form-item {
  margin-bottom: 15px;
}

.label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #64748b;
}

input {
  width: 100%;
  height: 40px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 0 10px;
  font-size: 14px;
}

.submit-btn {
  background-color: #007aff;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  padding: 10px;
  font-size: 14px;
  margin-top: 10px;
}

.record-list {
  flex: 1;
  margin: 0 15px;
  background-color: #ffffff;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 70px;
}

.list-header {
  font-weight: 600;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e2e8f0;
}

.empty-tip {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  color: #94a3b8;
}

.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #e2e8f0;
}

.record-info {
  display: flex;
  flex-direction: column;
}

.record-date {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 5px;
}

.record-value {
  font-size: 16px;
  font-weight: 500;
}

.delete-btn {
  color: #ef4444;
  font-size: 14px;
}

.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background-color: #ffffff;
  display: flex;
  justify-content: space-around;
  align-items: center;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  height: 100%;
}

.nav-icon {
  font-size: 22px;
  margin-bottom: 4px;
}

.nav-text {
  font-size: 12px;
  color: #64748b;
}

.active {
  color: #007aff;
}

.active .nav-text {
  color: #007aff;
}

slider {
  margin: 10px 0;
}
</style>
