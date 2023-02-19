import http from '../core/http.js'

const articleDatumService = {
  prefix: '',
  getUrl(url) {
    return this.prefix + url
  },

  async getArticleDatums(articleId) {
    let url = this.getUrl(`/article/${articleId}/datum`)
    return await http.get(url)
  },

  async createArticleDatum(articleId, data) {
    let url = this.getUrl(`/article/${articleId}/datum`)
    return await http.postFormData(url, data)
  },



}

export default articleDatumService
