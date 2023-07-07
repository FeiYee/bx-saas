import http from '../core/http.js'

const excelService = {
  prefix: '',
  getUrl(url) {
    return this.prefix + url
  },

  async getArticleExcelByKeyword(keyword) {
    let data = {
      keyword
    }
    let url = this.getUrl(`/excel/article`)
    return await http.get(url, data)
  },


}

export default excelService
