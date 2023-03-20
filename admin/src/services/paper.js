import http from '../core/http.js'

const paperService = {
  prefix: '',
  getUrl(url) {
    return this.prefix + url
  },

  async getPapers(data) {
    let url = this.getUrl('/paper')
    return await http.get(url, data)
  },
  async createPaper(data) {
    let url = this.getUrl('/paper')
    return await http.postFormData(url, data)
  },
  async updatePaper(data) {
    let id = data.id
    let url = this.getUrl(`/paper/${id}`)
    return await http.putFormData(url, data)
  },
  async deletePaper(id) {
    let url = this.getUrl(`/paper/${id}`)
    return await http.delete(url)
  },
  async download(data) {
    let url = this.getUrl('/paper/download')
    return await http.delete(url, data)
  },

}

export default paperService
