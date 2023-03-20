import http from '../core/http.js'

const paperService = {
  prefix: '',
  getUrl(url) {
    return this.prefix + url
  },

  async getPaperDatums(paperId) {
    let url = this.getUrl(`/paper/${paperId}/datum`)
    return await http.get(url)
  },
  async createPaperDatum(paperId, data) {
    let url = this.getUrl(`/paper/${paperId}/datum`)
    return await http.postFormData(url, data)
  },
  async updatePaperDatum(data) {
    let id = data.id
    let url = this.getUrl(`/paper/datum/${id}`)
    return await http.putFormData(url, data)
  },
  async deletePaperDatum(id) {
    let url = this.getUrl(`/paper/datum/${id}`)
    return await http.delete(url)
  },
  async download(data) {
    let url = this.getUrl('/paper/download')
    return await http.delete(url, data)
  },

}

export default paperService
