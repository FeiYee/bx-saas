import http from '../core/http.js'

const keywordService = {
  prefix: '',
  getUrl(url) {
    return this.prefix + url
  },

  async getUserKeywords() {
    let url = this.getUrl(`/keyword/user`)
    return await http.get(url)
  },

  async deleteKeyword(id) {
    let url = this.getUrl(`/keyword/${id}`)
    return await http.delete(url)
  }


}

export default keywordService
