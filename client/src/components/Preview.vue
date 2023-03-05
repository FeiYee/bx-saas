<template>
  <section class="preview">
    <div class="preview-content">
      <div class="preview-img" v-show="file.type === 0">
        <img :src="file.url" srcset="">
      </div>
      <div v-show="file.type === 1" id="excel"></div>
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
      <div class="preview-operate-download" @click="onClickExport">
        <span>导出</span>
        <el-icon><Download color="#9E9E9E"/></el-icon>
      </div>
    </div>
  </section>
</template>
<script setup>
import { ref, defineEmits, computed, watch } from 'vue'
import { read, utils, writeFile } from 'xlsx';
import canvasDatagrid from 'canvas-datagrid';

const props = defineProps({
  modelValue: Array,
});

const file = ref({});
const fileIndex = ref(0);

const fileList = computed({
  get: () => props.modelValue,
  set: (value) => {
    emit('update:modelValue', value)
  }
});

const emit = defineEmits(['update:modelValue', 'export']);

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
};

const onClickExport = () => {
  emit('export')
};

const renderExcel = async (file) => {
  let url = file.value.url;

  const dom = document.getElementById('excel');
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

  grid.style.height = '330px';
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
  height: 432px;
  padding: 20px;

  .preview-content {
    height: 332px;
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
