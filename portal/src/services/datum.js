import http from '../core/http.js'

const datumService = {
  prefix: '',
  getUrl(url) {
    return this.prefix + url
  },

  async getDatums(data) {
    let url = this.getUrl('/datum')
    return await http.get(url, data)
  },
  async createDatum(data) {
    let url = this.getUrl('/datum')
    return await http.postFormData(url, data)
  },
  async updateDatum(data) {
    let id = data.id
    let url = this.getUrl(`/datum/${id}`)
    return await http.put(url, data)
  },
  async deleteDatum(id) {
    let url = this.getUrl(`/datum/${id}`)
    return await http.delete(url)
  },
  async download(data) {
    let url = this.getUrl('/datum/download')
    return await http.delete(url, data)
  },
  async downloadExcel(data) {
    let url = this.getUrl('/datum/download/excel')
    return await http.delete(url, data)
  },

  async getArticleTitle(title) {
    let data = {
      title
    }
    let url = this.getUrl('/article/title')
    return await http.get(url, data)
  }

}

export default datumService
