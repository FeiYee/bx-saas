import http from '../core/http.js'

const keywordService = {
  prefix: '',
  getUrl(url) {
    return this.prefix + url
  },

  async getUserKeywords(searchType) {
    let data = {
      search_type: searchType
    }
    let url = this.getUrl(`/keyword/user`)
    return await http.get(url, data)
  },

  async deleteKeyword(id) {
    let url = this.getUrl(`/keyword/${id}`)
    return await http.delete(url)
  }


}

export default keywordService
