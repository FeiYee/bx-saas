import { filePrefix } from "./config"


export const downloadFile = function (url, fileName) {
  const ele = document.createElement('a')
  if (!url.startsWith(filePrefix)) {
    url = filePrefix + url;
  }
  ele.href = url
  ele.setAttribute('download', fileName || '')
  ele.style.display = 'none'
  document.body.appendChild(ele)
  setTimeout(() => {
    ele.click()
    document.body.removeChild(ele)
  }, 66)
}

// export const downloadExcelFile = function (url, fileName) {
//   const ele = document.createElement('a')
//   ele.href = downloadFile + url
//   ele.setAttribute('download', fileName || '')
//   ele.style.display = 'none'
//   document.body.appendChild(ele)
//   setTimeout(() => {
//     ele.click()
//     document.body.removeChild(ele)
//   }, 66)
// }
