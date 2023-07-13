<template>
  <section class="preview">
    <div class="preview-content">
      <div class="preview-img" v-show="file.type === 0">
        <img v-if="file.type === 0" :src="file.url">
        <!-- <ElImage v-if="file.type === 0" :src="file.url" :zoom-rate="1.2" :preview-src-list="[file.url]" style="height: 100%;" fit="scale-down"></ElImage> -->
      </div>
      <div v-show="file.type === 1" id="excel" ref="excelDom"></div>
    </div>
    <div class="preview-operate" >
      <div class="preview-operate-page">
        <span
          v-for="(item, index) in fileList"
          :key="index" @click="onClick(index)"
          :class="{active: fileIndex === index}">
          {{ index + 1 }}
        </span>
      </div>
      <div class="preview-operate-download" @click="onClickExport" v-if="!isExportDisabled">
        <span>导出</span>
        <el-icon><Download color="#9E9E9E"/></el-icon>
      </div>
    </div>
  </section>
</template>
<script setup>
import { ref, defineEmits, computed, watch, onMounted } from 'vue'
import { ElImage } from 'element-plus'
import { read, utils, writeFile } from 'xlsx';
import canvasDatagrid from 'canvas-datagrid';

const props = defineProps({
  modelValue: Array,
  currentValue: Object,
  isExportDisabled: {
    type: Boolean,
    default: false
  },
});

const file = ref({});
const fileIndex = ref(0);

const excelDom = ref(null);

const fileList = computed({
  get: () => props.modelValue,
  set: (value) => {
    emit('update:modelValue', value)
  }
});

const emit = defineEmits(['update:modelValue', 'update:currentValue', 'export']);

watch(
  () => props.modelValue,
  value => {
    if (value) {
      onClick(0)
    }
  }
)


const onClick = (index) => {
  if (!fileList.value.length) {
    return
  }
  fileIndex.value = index;
  file.value = fileList.value[index];
  if (file.value.type === 1) {
    renderExcel(file)
  }
  emit('update:currentValue', file.value)
};

const onClickExport = () => {
  emit('export')
};

onMounted(() => {
  init()
});


const init = () => {
  onClick(0)
};


const renderExcel = async (file) => {
  let url = file.value.url;

  // const dom = document.getElementById('excel');
  const dom = excelDom.value;
  const res = await fetch(url, {mode: 'no-cors'});
  const buffer = await res.arrayBuffer();
  const wb = read(buffer, {type: 'array'});
  const ws = wb.Sheets[wb.SheetNames[0]];
  const data = utils.sheet_to_json(ws, {header:1});

  dom.innerHTML = '';
  const grid = canvasDatagrid({
    parentNode: dom,
    data: data
  });

  grid.style.height = '348px';
  grid.style.width = '100%';

  /* create schema (for A,B,C column headings) */
  let range = utils.decode_range(ws['!ref']);
  for(let i = range.s.c; i <= range.e.c; ++i) {
    grid.schema[i - range.s.c].title = utils.encode_col(i);
  }

};


</script>
<style lang="scss">
.preview {
  width: 100%;
  // height: 432px;
  // padding: 20px;

  .preview-content {
    height: 350px;
    border: 1px solid #e3e3e3;
  }

  .preview-img {
    width: 100%;
    height: 100%;
    max-height: 100%;
    max-width: 100%;
    text-align: center;
    img {
      // width: 100%;
      height: 100%;
    }
  }

  .preview-operate {
    height: 3rem;
    text-align: center;
    padding-top: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: auto;
  }

  .preview-operate-page {
    display: flex;
    span {
      display: inline-block;
      padding: 0 6px;
      font-size: 1.2rem;
      cursor: pointer;
      &.active {
        color: var(--color-primary);
      }
    }
  }
  .preview-operate-download {
    display: flex;
    align-items: center;
    font-size: 1.2rem;
    padding-left: 1rem;
    cursor: pointer;
    span {
      color: var(--color-primary);
    }


  }


}
</style>
