<template>
  <section class="preview">
    <div class="preview-content">
      <div class="preview-img" v-show="file.type === 0">
        <img :src="file.url" srcset="">
        <!-- <el-image
          style="width: 100%; height: 100%"
          :src="file.url"
          :zoom-rate="1.2"
          :preview-src-list="file.url"
          :initial-index="4"
          fit="cover"
        /> -->
      </div>
      <div v-show="file.type === 1" id="excel"></div>
    </div>
    <div class="preview-operate" >
      <span v-for="(item, index) in fileList" @click="onClick(index)">{{ index + 1 }}</span>
    </div>

  </section>
</template>
<script setup>
import { ref, defineEmits, computed, onMounted } from 'vue'
import { read, utils, writeFile } from 'xlsx';
import canvasDatagrid from 'canvas-datagrid';
// import context from '../core/context.js'

const props = defineProps({
  modelValue: String,
});

const emit = defineEmits(['search', 'update:modelValue']);

const keyword = computed({
  get: () => props.modelValue,
  set: (value) => {
    emit('update:modelValue', value)
  }
});


const file = ref({});

const fileList = ref([]);


const init = async () => {
  getFiles();

}

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

}


const getFiles = async () => {
  // fileList.value = [];
  // type: 0-> image, 1->excel

  fileList.value = [
    {
      url: 'http://localhost:8000/file/asset/1/xlsx/3.xlsx',
      type: 1,
    },
    {
      url: 'http://localhost:8000/file/asset/1/png/img_1.png',
      type: 0,
    },
    {
      url: 'http://localhost:8000/file/asset/1/png/img_2.png',
      type: 0,
    },
    {
      url: 'http://localhost:8000/file/asset/1/xlsx/1.xlsx',
      type: 1,
    }
  ]

}

const onClick = (index) => {
  file.value = fileList.value[index];

  console.log(file.value)
  if (file.value.type === 1) {
    renderExcel(file)
  }
}


init();

onMounted(() => {
  onClick(0);

})
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
    img {
      width: 100%;
      height: 100%;
    }
  }

  .preview-operate {
    text-align: center;
    padding-top: 1rem;
    span {
      display: inline-block;
      padding: 4px 6px;
      font-size: 1.5rem;
      cursor: pointer;
      &.active {
        color: var(--color-primary);
      }
    }
  }
}
</style>
