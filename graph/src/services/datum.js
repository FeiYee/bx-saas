import http from '../core/http.js'

const datumService = {
  prefix: '',
  getUrl(url) {
    return this.prefix + url
  },

  async getDatumByArticle(articleId) {
    let url = this.getUrl(`/datum/article/${articleId}`)
    return await http.get(url)
  },

  async download(title) {
    let data = {
      title
    }
    let url = this.getUrl('/datum/download')
    return await http.get(url, data)
  },

  async downloadExcel(keyword) {
    let data = {
      keyword
    }
    let url = this.getUrl('/datum/download/excel')
    return await http.get(url, data)
  },

}

export default datumService
