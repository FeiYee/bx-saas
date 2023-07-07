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

  async deleteArticleDatum(articleDatumId) {
    let url = this.getUrl(`/article/datum/${articleDatumId}`)
    return await http.delete(url)
  },

  async uploadArticleDatum(data) {
    let url = this.getUrl(`/article/datum/upload`)
    return await http.postFormData(url, data)
  },

  async getArticleDatumsByUser(data) {
    let url = this.getUrl(`/article/datum/user`)
    return await http.get(url, data)
  },

}

export default articleDatumService
