import http from '../core/http.js'

const searchService = {
  prefix: '',
  getUrl(url) {
    return this.prefix + url
  },


  async searchGraph(data) {
    let url = this.getUrl('/search/graph')
    return await http.get(url, data)
  },

  async searchArticle(data) {
    let url = this.getUrl('/search/article')
    return await http.get(url, data)
  },

  async getKeywords(data) {
    let url = this.getUrl('/keyword')
    return await http.get(url, data)
  },
  async createKeyword(data) {
    let url = this.getUrl('/keyword')
    return await http.post(url, data)
  },
  async updateKeyword(data) {
    let id = data.id
    let url = this.getUrl(`/keyword/${id}`)
    return await http.put(url, data)
  },
  async deleteKeyword(id) {
    let url = this.getUrl(`/keyword/${id}`)
    return await http.delete(url)
  },


}

export default searchService
