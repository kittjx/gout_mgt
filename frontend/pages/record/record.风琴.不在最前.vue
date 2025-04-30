<template>
  <view class="container">
    <view class="header">
      <text class="title">记录信息</text>
    </view>

    <view class="accordion-container">
      <view class="accordion-item">
        <view class="accordion-header" @click="toggleAccordion('weight')">
          <text class="accordion-title">体重记录</text>
          <text class="accordion-icon">{{ openSections.weight ? '▼' : '►' }}</text>
        </view>
        <view class="accordion-content" v-if="openSections.weight">
          <view v-if="userRecords.weight.length === 0" class="empty-message">
            <text>暂无记录，点击下方的 "+" 添加</text>
          </view>
          <view v-else class="record-list">
            <view v-for="(item, index) in userRecords.weight" :key="index" class="record-item">
              <view class="record-info">
                <text class="record-date">{{ formatDate(item.date) }}</text>
                <text class="record-value">{{ item.value }}kg</text>
              </view>
              <view class="record-actions">
                <text class="delete-btn" @click="deleteRecord('weight', index)">删除</text>
              </view>
            </view>
          </view>
          <view class="add-record-in-section" @click="openAddModal('体重')">
            <text class="add-icon">+</text>
            <text>添加体重记录</text>
          </view>
        </view>
      </view>

      <view class="accordion-item">
         <view class="accordion-header" @click="toggleAccordion('mainFood')">
           <text class="accordion-title">主食记录</text>
           <text class="accordion-icon">{{ openSections.mainFood ? '▼' : '►' }}</text>
         </view>
         <view class="accordion-content" v-if="openSections.mainFood">
           <view v-if="userRecords.mainFood.length === 0" class="empty-message">
             <text>暂无记录，点击下方的 "+" 添加</text>
           </view>
           <view v-else class="record-list">
             <view v-for="(item, index) in userRecords.mainFood" :key="index" class="record-item">
               <view class="record-info">
                 <text class="record-date">{{ formatDate(item.date) }}</text>
                 <text class="record-value">{{ item.name }} - {{ item.amount }}</text>
               </view>
               <view class="record-actions">
                 <text class="delete-btn" @click="deleteRecord('mainFood', index)">删除</text>
               </view>
             </view>
           </view>
           <view class="add-record-in-section" @click="openAddModal('主食')">
             <text class="add-icon">+</text>
             <text>添加主食记录</text>
           </view>
         </view>
       </view>

       <view class="accordion-item">
         <view class="accordion-header" @click="toggleAccordion('waterIntake')">
           <text class="accordion-title">饮水量记录</text>
           <text class="accordion-icon">{{ openSections.waterIntake ? '▼' : '►' }}</text>
         </view>
         <view class="accordion-content" v-if="openSections.waterIntake">
           <view v-if="userRecords.waterIntake.length === 0" class="empty-message">
             <text>暂无记录，点击下方的 "+" 添加</text>
           </view>
           <view v-else class="record-list">
             <view v-for="(item, index) in userRecords.waterIntake" :key="index" class="record-item">
               <view class="record-info">
                 <text class="record-date">{{ formatDate(item.date) }}</text>
                 <text class="record-value">{{ item.amount }}ml</text>
               </view>
               <view class="record-actions">
                 <text class="delete-btn" @click="deleteRecord('waterIntake', index)">删除</text>
               </view>
             </view>
           </view>
           <view class="add-record-in-section" @click="openAddModal('饮水量')">
             <text class="add-icon">+</text>
             <text>添加饮水量记录</text>
           </view>
         </view>
       </view>

      <view class="accordion-item">
        <view class="accordion-header" @click="toggleAccordion('purineFood')">
          <text class="accordion-title">高嘌呤饮食</text>
          <text class="accordion-icon">{{ openSections.purineFood ? '▼' : '►' }}</text>
        </view>
        <view class="accordion-content" v-if="openSections.purineFood">
          <view v-if="userRecords.purineFood.length === 0" class="empty-message">
            <text>暂无记录，点击下方的 "+" 添加</text>
          </view>
          <view v-else class="record-list">
            <view v-for="(item, index) in userRecords.purineFood" :key="index" class="record-item">
               <view class="record-info">
                <text class="record-date">{{ formatDate(item.date) }}</text>
                <text class="record-value">{{ item.type }} - {{ item.amount }}</text>
              </view>
              <view class="record-actions">
                <text class="delete-btn" @click="deleteRecord('purineFood', index)">删除</text>
              </view>
            </view>
          </view>
           <view class="add-record-in-section" @click="openAddModal('高嘌呤饮食')">
            <text class="add-icon">+</text>
            <text>添加高嘌呤饮食记录</text>
          </view>
        </view>
      </view>

      <view class="accordion-item">
        <view class="accordion-header" @click="toggleAccordion('uricAcid')">
          <text class="accordion-title">尿酸监测</text>
          <text class="accordion-icon">{{ openSections.uricAcid ? '▼' : '►' }}</text>
        </view>
        <view class="accordion-content" v-if="openSections.uricAcid">
          <view v-if="userRecords.uricAcid.length === 0" class="empty-message">
             <text>暂无记录，点击下方的 "+" 添加</text>
          </view>
          <view v-else class="record-list">
            <view v-for="(item, index) in userRecords.uricAcid" :key="index" class="record-item">
               <view class="record-info">
                <text class="record-date">{{ formatDate(item.date) }}</text>
                <text class="record-value">{{ item.value }}μmol/L ({{ item.method }})</text>
              </view>
              <view class="record-actions">
                <text class="delete-btn" @click="deleteRecord('uricAcid', index)">删除</text>
              </view>
            </view>
          </view>
           <view class="add-record-in-section" @click="openAddModal('尿酸监测')">
            <text class="add-icon">+</text>
            <text>添加尿酸监测记录</text>
          </view>
        </view>
      </view>

      <view class="accordion-item">
        <view class="accordion-header" @click="toggleAccordion('urinePH')">
          <text class="accordion-title">尿液酸碱值</text>
          <text class="accordion-icon">{{ openSections.urinePH ? '▼' : '►' }}</text>
        </view>
        <view class="accordion-content" v-if="openSections.urinePH">
          <view v-if="userRecords.urinePH.length === 0" class="empty-message">
             <text>暂无记录，点击下方的 "+" 添加</text>
          </view>
          <view v-else class="record-list">
            <view v-for="(item, index) in userRecords.urinePH" :key="index" class="record-item">
               <view class="record-info">
                <text class="record-date">{{ formatDate(item.date) }}</text>
                <text class="record-value">pH {{ item.value }}</text>
              </view>
              <view class="record-actions">
                <text class="delete-btn" @click="deleteRecord('urinePH', index)">删除</text>
              </view>
            </view>
          </view>
           <view class="add-record-in-section" @click="openAddModal('尿液酸碱值')">
            <text class="add-icon">+</text>
            <text>添加尿液酸碱值记录</text>
          </view>
        </view>
      </view>

      <view class="accordion-item">
        <view class="accordion-header" @click="toggleAccordion('examinations')">
          <text class="accordion-title">检查记录</text>
          <text class="accordion-icon">{{ openSections.examinations ? '▼' : '►' }}</text>
        </view>
        <view class="accordion-content" v-if="openSections.examinations">
          <view v-if="userRecords.examinations.length === 0" class="empty-message">
            <text>暂无记录，点击下方的 "+" 添加</text>
          </view>
          <view v-else class="record-list">
            <view v-for="(item, index) in userRecords.examinations" :key="index" class="record-item">
               <view class="record-info">
                <text class="record-date">{{ formatDate(item.date) }}</text>
                <text class="record-value">{{ item.type }}: {{ item.value }}</text>
              </view>
              <view class="record-actions">
                <text class="delete-btn" @click="deleteRecord('examinations', index)">删除</text>
              </view>
            </view>
          </view>
           <view class="add-record-in-section" @click="openAddModal('检查记录')">
            <text class="add-icon">+</text>
            <text>添加检查记录</text>
          </view>
        </view>
      </view>

      <view class="accordion-item">
        <view class="accordion-header" @click="toggleAccordion('attack')">
          <text class="accordion-title">发作情况</text>
          <text class="accordion-icon">{{ openSections.attack ? '▼' : '►' }}</text>
        </view>
        <view class="accordion-content" v-if="openSections.attack">
          <view v-if="userRecords.attack.length === 0" class="empty-message">
            <text>暂无记录，点击下方的 "+" 添加</text>
          </view>
          <view v-else class="record-list">
            <view v-for="(item, index) in userRecords.attack" :key="index" class="record-item">
               <view class="record-info">
                <text class="record-date">{{ formatDate(item.date) }}</text>
                <text class="record-value">持续: {{ item.duration }}小时, 疼痛评分: {{ item.painScore }}/10</text>
              </view>
              <view class="record-actions">
                <text class="delete-btn" @click="deleteRecord('attack', index)">删除</text>
              </view>
            </view>
          </view>
           <view class="add-record-in-section" @click="openAddModal('发作情况')">
            <text class="add-icon">+</text>
            <text>添加发作情况记录</text>
          </view>
        </view>
      </view>

      <view class="accordion-item">
        <view class="accordion-header" @click="toggleAccordion('tophi')">
          <text class="accordion-title">痛风石直径</text>
          <text class="accordion-icon">{{ openSections.tophi ? '▼' : '►' }}</text>
        </view>
        <view class="accordion-content" v-if="openSections.tophi">
          <view v-if="userRecords.tophi.length === 0" class="empty-message">
            <text>暂无记录，点击下方的 "+" 添加</text>
          </view>
          <view v-else class="record-list">
            <view v-for="(item, index) in userRecords.tophi" :key="index" class="record-item">
               <view class="record-info">
                <text class="record-date">{{ formatDate(item.date) }}</text>
                <text class="record-value">{{ item.location }}: {{ item.diameter }}mm</text>
              </view>
              <view class="record-actions">
                <text class="delete-btn" @click="deleteRecord('tophi', index)">删除</text>
              </view>
            </view>
          </view>
           <view class="add-record-in-section" @click="openAddModal('痛风石直径')">
            <text class="add-icon">+</text>
            <text>添加痛风石记录</text>
          </view>
        </view>
      </view>

       <view class="accordion-item">
        <view class="accordion-header" @click="toggleAccordion('jointFunction')">
          <text class="accordion-title">关节功能</text>
          <text class="accordion-icon">{{ openSections.jointFunction ? '▼' : '►' }}</text>
        </view>
        <view class="accordion-content" v-if="openSections.jointFunction">
          <view v-if="userRecords.jointFunction.length === 0" class="empty-message">
            <text>暂无记录，点击下方的 "+" 添加</text>
          </view>
          <view v-else class="record-list">
            <view v-for="(item, index) in userRecords.jointFunction" :key="index" class="record-item">
               <view class="record-info">
                <text class="record-date">{{ formatDate(item.date) }}</text>
                <text class="record-value">{{ item.joint }}: {{ item.description }}</text>
              </view>
              <view class="record-actions">
                <text class="delete-btn" @click="deleteRecord('jointFunction', index)">删除</text>
              </view>
            </view>
          </view>
           <view class="add-record-in-section" @click="openAddModal('关节功能')">
            <text class="add-icon">+</text>
            <text>添加关节功能记录</text>
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
            <text class="form-label">记录日期</text>
            <picker mode="date" :value="selectedDate" @change="onDateChange" class="picker">
              <view class="picker-value">{{ selectedDate }}</view>
            </picker>
          </view>

          <view class="form-item">
            <text class="form-label">记录时间</text>
            <picker mode="time" :value="selectedTime" @change="onTimeChange" class="picker">
              <view class="picker-value">{{ selectedTime }}</view>
            </picker>
          </view>

          <view v-if="currentRecordType === '体重'">
             <view class="form-item">
               <text class="form-label">体重 (kg)</text>
               <input type="digit" v-model="newRecord.weight.value" placeholder="请输入体重" class="input" />
             </view>
           </view>

           <view v-if="currentRecordType === '主食'">
             <view class="form-item">
               <text class="form-label">食物名称</text>
               <input type="text" v-model="newRecord.mainFood.name" placeholder="请输入食物名称" class="input" />
             </view>
             <view class="form-item">
               <text class="form-label">食用量</text>
               <input type="text" v-model="newRecord.mainFood.amount" placeholder="例如: 1碗/100g" class="input" />
             </view>
           </view>

           <view v-if="currentRecordType === '饮水量'">
             <view class="form-item">
               <text class="form-label">饮水量 (ml)</text>
               <input type="digit" v-model="newRecord.waterIntake.amount" placeholder="请输入饮水量" class="input" />
             </view>
           </view>

           <view v-if="currentRecordType === '高嘌呤饮食'">
             <view class="form-item">
               <text class="form-label">食物类型</text>
               <input type="text" v-model="newRecord.purineFood.type" placeholder="例如: 海鲜/红肉" class="input" />
             </view>
             <view class="form-item">
               <text class="form-label">食用量</text>
               <input type="text" v-model="newRecord.purineFood.amount" placeholder="例如: 100g" class="input" />
             </view>
           </view>

           <view v-if="currentRecordType === '尿酸监测'">
             <view class="form-item">
               <text class="form-label">尿酸值 (μmol/L)</text>
               <input type="digit" v-model="newRecord.uricAcid.value" placeholder="请输入尿酸值" class="input" />
             </view>
             <view class="form-item">
               <text class="form-label">检测方式</text>
               <picker :range="['血液检测', '自测仪']" @change="onUricAcidMethodChange" class="picker">
                 <view class="picker-value">{{ newRecord.uricAcid.method || '请选择检测方式' }}</view>
               </picker>
             </view>
           </view>

           <view v-if="currentRecordType === '尿液酸碱值'">
             <view class="form-item">
               <text class="form-label">pH值</text>
               <input type="digit" v-model="newRecord.urinePH.value" placeholder="请输入pH值" class="input" />
             </view>
           </view>

           <view v-if="currentRecordType === '检查记录'">
             <view class="form-item">
               <text class="form-label">检查类型</text>
               <picker :range="['肝功能', '肾功能', '血糖', '血压', '血脂']" @change="onExaminationTypeChange" class="picker">
                 <view class="picker-value">{{ newRecord.examinations.type || '请选择检查类型' }}</view>
               </picker>
             </view>
             <view class="form-item">
               <text class="form-label">检查值</text>
               <input type="text" v-model="newRecord.examinations.value" placeholder="请输入检查结果" class="input" />
             </view>
           </view>

           <view v-if="currentRecordType === '发作情况'">
             <view class="form-item">
               <text class="form-label">持续时间 (小时)</text>
               <input type="digit" v-model="newRecord.attack.duration" placeholder="请输入发作持续时间" class="input" />
             </view>
             <view class="form-item">
               <text class="form-label">疼痛评分 (1-10)</text>
               <slider v-model="newRecord.attack.painScore" min="1" max="10" show-value class="slider" />
             </view>
           </view>

           <view v-if="currentRecordType === '痛风石直径'">
             <view class="form-item">
               <text class="form-label">部位</text>
               <input type="text" v-model="newRecord.tophi.location" placeholder="例如: 左脚大拇指" class="input" />
             </view>
             <view class="form-item">
               <text class="form-label">直径 (mm)</text>
               <input type="digit" v-model="newRecord.tophi.diameter" placeholder="请输入直径" class="input" />
             </view>
           </view>

           <view v-if="currentRecordType === '关节功能'">
             <view class="form-item">
               <text class="form-label">关节</text>
               <input type="text" v-model="newRecord.jointFunction.joint" placeholder="例如: 左膝关节" class="input" />
             </view>
             <view class="form-item">
               <text class="form-label">功能描述</text>
               <textarea v-model="newRecord.jointFunction.description" placeholder="请输入关节功能描述" class="textarea" />
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
import { ref, reactive } from 'vue';

// 记录类型 (Still used for mapping and potentially display)
const recordTypes = [
  '体重', '主食', '饮水量', '高嘌呤饮食',
  '尿酸监测', '尿液酸碱值', '检查记录',
  '发作情况', '痛风石直径', '关节功能'
];

// 当前选择的记录类型 (Set by openAddModal)
const currentRecordType = ref('');

// 控制新增记录弹窗的显示
const showAddRecordModal = ref(false);

// *** Added state for Date/Time Pickers ***
const selectedDate = ref('');
const selectedTime = ref('');

// Helper to get current date/time formatted for pickers
const getCurrentFormattedDateTime = () => {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    return {
        date: `${year}-${month}-${day}`,
        time: `${hours}:${minutes}`
    };
};


// 控制手风琴展开状态
const openSections = reactive({
  weight: true,
  mainFood: false,
  waterIntake: false,
  purineFood: false,
  uricAcid: false,
  urinePH: false,
  examinations: false,
  attack: false,
  tophi: false,
  jointFunction: false
});

// 用户记录数据
const userRecords = reactive({
   weight: [ { date: new Date('2025-04-18T10:30:00'), value: 75.5 }, { date: new Date('2025-04-15T09:00:00'), value: 76.2 } ],
   mainFood: [ { date: new Date('2025-04-19T12:00:00'), name: '米饭', amount: '1碗' } ],
   waterIntake: [ { date: new Date('2025-04-20T14:00:00'), amount: 2000 } ],
   purineFood: [],
   uricAcid: [ { date: new Date('2025-04-10T08:00:00'), value: 420, method: '血液检测' } ],
   urinePH: [],
   examinations: [],
   attack: [ { date: new Date('2025-04-05T20:00:00'), duration: 6, painScore: 8 } ],
   tophi: [],
   jointFunction: []
 });

// 新记录对象
const newRecord = reactive({
  weight: { value: '' },
  mainFood: { name: '', amount: '' },
  waterIntake: { amount: '' },
  purineFood: { type: '', amount: '' },
  uricAcid: { value: '', method: '' },
  urinePH: { value: '' },
  examinations: { type: '', value: '' },
  attack: { duration: '', painScore: 5 },
  tophi: { location: '', diameter: '' },
  jointFunction: { joint: '', description: '' }
});

// 切换手风琴面板
const toggleAccordion = (section) => {
  openSections[section] = !openSections[section];
};

// 打开模态框并设置类型和默认时间
const openAddModal = (recordType) => {
  currentRecordType.value = recordType;
  const { date, time } = getCurrentFormattedDateTime(); // Get current date/time
  selectedDate.value = date; // Set default date
  selectedTime.value = time; // Set default time
  resetNewRecordFields(recordType);
  showAddRecordModal.value = true;
};

// Helper function to reset specific fields
const resetNewRecordFields = (type) => {
    Object.keys(newRecord).forEach(key => {
        Object.keys(newRecord[key]).forEach(field => {
            if (field === 'painScore') {
                 newRecord[key][field] = 5;
            } else {
                newRecord[key][field] = '';
            }
        });
    });
     if (type === '尿酸监测') newRecord.uricAcid.method = '';
     if (type === '检查记录') newRecord.examinations.type = '';
};

// *** Handlers for Date/Time Pickers ***
const onDateChange = (e) => {
  selectedDate.value = e.detail.value;
};

const onTimeChange = (e) => {
  selectedTime.value = e.detail.value;
};

// 尿酸监测方式改变事件
const onUricAcidMethodChange = (e) => {
  const methods = ['血液检测', '自测仪'];
  newRecord.uricAcid.method = methods[e.detail.value];
};

// 检查类型改变事件
const onExaminationTypeChange = (e) => {
  const types = ['肝功能', '肾功能', '血糖', '血压', '血脂'];
  newRecord.examinations.type = types[e.detail.value];
};

// 添加记录 - Now uses selectedDate and selectedTime
const addRecord = () => {
  // *** Construct Date object from pickers ***
  if (!selectedDate.value || !selectedTime.value) {
      uni.showToast({ title: '请选择记录日期和时间', icon: 'none' });
      return;
  }
  // Basic check for common formats, adjust if needed
  const dateTimeString = `${selectedDate.value} ${selectedTime.value}`;
  const recordDate = new Date(dateTimeString.replace(/-/g, '/')); // Replace hyphens for broader compatibility if needed


  // Validate constructed date
  if (isNaN(recordDate.getTime())) {
       uni.showToast({ title: '日期或时间格式无效', icon: 'none' });
       console.error("Invalid date constructed:", dateTimeString);
       return;
  }

  const typeMap = {
     '体重': 'weight', '主食': 'mainFood', '饮水量': 'waterIntake', '高嘌呤饮食': 'purineFood',
     '尿酸监测': 'uricAcid', '尿液酸碱值': 'urinePH', '检查记录': 'examinations',
     '发作情况': 'attack', '痛风石直径': 'tophi', '关节功能': 'jointFunction'
  };
  const recordKey = typeMap[currentRecordType.value];

  if (!recordKey) {
      console.error("Invalid record type selected:", currentRecordType.value);
      uni.showToast({ title: '无效的记录类型', icon: 'none' });
      return;
  }

  let recordAdded = false;

  // *** Use 'recordDate' instead of 'now' in all cases below ***
  switch (currentRecordType.value) {
    case '体重':
      if (newRecord.weight.value && !isNaN(parseFloat(newRecord.weight.value))) {
        userRecords.weight.unshift({ date: recordDate, value: parseFloat(newRecord.weight.value) }); // Use recordDate
        recordAdded = true;
      }
      break;
    case '主食':
      if (newRecord.mainFood.name && newRecord.mainFood.amount) {
        userRecords.mainFood.unshift({ date: recordDate, name: newRecord.mainFood.name, amount: newRecord.mainFood.amount }); // Use recordDate
         recordAdded = true;
      }
      break;
    case '饮水量':
       if (newRecord.waterIntake.amount && !isNaN(parseInt(newRecord.waterIntake.amount))) {
        userRecords.waterIntake.unshift({ date: recordDate, amount: parseInt(newRecord.waterIntake.amount) }); // Use recordDate
         recordAdded = true;
      }
      break;
     case '高嘌呤饮食':
       if (newRecord.purineFood.type && newRecord.purineFood.amount) {
         userRecords.purineFood.unshift({ date: recordDate, type: newRecord.purineFood.type, amount: newRecord.purineFood.amount }); // Use recordDate
          recordAdded = true;
       }
       break;
     case '尿酸监测':
       if (newRecord.uricAcid.value && !isNaN(parseFloat(newRecord.uricAcid.value)) && newRecord.uricAcid.method) {
         userRecords.uricAcid.unshift({ date: recordDate, value: parseFloat(newRecord.uricAcid.value), method: newRecord.uricAcid.method }); // Use recordDate
          recordAdded = true;
       }
       break;
      case '尿液酸碱值':
        if (newRecord.urinePH.value && !isNaN(parseFloat(newRecord.urinePH.value))) {
          userRecords.urinePH.unshift({ date: recordDate, value: parseFloat(newRecord.urinePH.value) }); // Use recordDate
           recordAdded = true;
        }
        break;
      case '检查记录':
        if (newRecord.examinations.type && newRecord.examinations.value) {
          userRecords.examinations.unshift({ date: recordDate, type: newRecord.examinations.type, value: newRecord.examinations.value }); // Use recordDate
           recordAdded = true;
        }
        break;
       case '发作情况':
         if (newRecord.attack.duration && !isNaN(parseFloat(newRecord.attack.duration))) {
           userRecords.attack.unshift({ date: recordDate, duration: parseFloat(newRecord.attack.duration), painScore: parseInt(newRecord.attack.painScore) }); // Use recordDate
            recordAdded = true;
         }
         break;
       case '痛风石直径':
         if (newRecord.tophi.location && newRecord.tophi.diameter && !isNaN(parseFloat(newRecord.tophi.diameter))) {
           userRecords.tophi.unshift({ date: recordDate, location: newRecord.tophi.location, diameter: parseFloat(newRecord.tophi.diameter) }); // Use recordDate
            recordAdded = true;
         }
         break;
       case '关节功能':
         if (newRecord.jointFunction.joint && newRecord.jointFunction.description) {
           userRecords.jointFunction.unshift({ date: recordDate, joint: newRecord.jointFunction.joint, description: newRecord.jointFunction.description }); // Use recordDate
            recordAdded = true;
         }
         break;
  }

   if (recordAdded) {
        // Sort records after adding to maintain chronological order (newest first)
        if (userRecords[recordKey]) {
            userRecords[recordKey].sort((a, b) => b.date.getTime() - a.date.getTime());
        }

        showAddRecordModal.value = false;
        resetNewRecordFields(currentRecordType.value);
        currentRecordType.value = '';
   } else {
       uni.showToast({ title: '请填写完整的记录信息', icon: 'none' });
   }
};

// 删除记录
const deleteRecord = (typeOrKey, index) => {
   // Ensure we use the internal key ('weight', 'mainFood', etc.)
   const typeMap = {
       '体重': 'weight', '主食': 'mainFood', '饮水量': 'waterIntake', '高嘌呤饮食': 'purineFood',
       '尿酸监测': 'uricAcid', '尿液酸碱值': 'urinePH', '检查记录': 'examinations',
       '发作情况': 'attack', '痛风石直径': 'tophi', '关节功能': 'jointFunction'
   };
   // If 'typeOrKey' is a display name, map it; otherwise, assume it's already the key.
   const recordKey = typeMap[typeOrKey] || typeOrKey;

   uni.showModal({
     title: '确认删除',
     content: '确定要删除这条记录吗？',
     success: (res) => {
       if (res.confirm) {
          if(userRecords[recordKey] && userRecords[recordKey][index] !== undefined) {
             userRecords[recordKey].splice(index, 1);
          } else {
              console.error("Could not find record to delete at key:", recordKey, "index:", index);
              uni.showToast({ title: '删除失败', icon: 'none' });
          }
       }
     }
   });
 };

// 格式化日期
const formatDate = (date) => {
  if (!(date instanceof Date)) {
      // Attempt to convert from string/number if necessary
      const parsedDate = new Date(date);
      if (isNaN(parsedDate.getTime())) return '无效日期';
      date = parsedDate;
  }

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  // Optional: Check if it's today or yesterday for more friendly display
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
       // Show month and day for current year, otherwise full date
       if (year === today.getFullYear()) {
           return `${month}-${day} ${hours}:${minutes}`;
       } else {
            return `${year}-${month}-${day} ${hours}:${minutes}`;
       }
  }
};


// 页面导航函数
const navigateTo = (url) => {
  uni.navigateTo({
    url: url
  });
};

// Initialize default date/time on component setup (optional)
// const { date, time } = getCurrentFormattedDateTime();
// selectedDate.value = date;
// selectedTime.value = time;

</script>

<style>
/* Styles remain largely the same, ensure .picker looks good */
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: calc(56px + env(safe-area-inset-bottom)); /* Adjust for tab bar + safe area */
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
  padding-bottom: 10px; /* Add some padding at the bottom */
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
  max-height: 300px; /* Limit height for scroll */
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
  color: #666; /* Slightly darker for better readability */
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
  max-width: 400px; /* Max width on larger screens */
  max-height: 85vh; /* Limit height */
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
  background-color: #f9f9f9; /* Slight background tint */
}

.cancel-btn {
  margin-right: 12px;
  padding: 8px 16px;
  background-color: #f5f5f5;
  color: #666;
  border-radius: 4px;
  font-size: 14px;
  border: 1px solid #ddd; /* Add border */
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

.input, .textarea {
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
  padding: 8px 12px; /* Vertical padding for textarea */
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
  position: relative; /* Needed for pseudo-element */
}

.picker-value {
  font-size: 14px;
  color: #333;
  flex: 1;
  overflow: hidden; /* Prevent text overflow */
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

/* Tab bar styles */
.tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 56px;
  background-color: #ffffff;
  display: flex;
  box-shadow: 0 -2px 6px rgba(0, 0, 0, 0.05);
  z-index: 100;
  padding-bottom: constant(safe-area-inset-bottom);
  padding-bottom: env(safe-area-inset-bottom);
  height: calc(56px + constant(safe-area-inset-bottom));
  height: calc(56px + env(safe-area-inset-bottom));
}

.tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #999;
  padding-top: 4px;
}

.tab-icon {
  font-size: 20px;
  margin-bottom: 2px;
}

.tab-text {
  font-size: 12px;
}

.tab-item.active {
  color: #4a86e8;
}

</style>