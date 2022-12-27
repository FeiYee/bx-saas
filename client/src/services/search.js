import http from '../core/http.js'

const searchService = {
  prefix: '',
  getUrl(url) {
    return this.prefix + url
  },

  async searchGraph(keyword) {
    let data = {
      keyword
    }
    let url = this.getUrl('/search/graph')
    return await http.get(url, data)
  },

  async searchArticle(keyword, topLevel) {
    let data = {
      keyword,
      top_level: topLevel
    }
    let url = this.getUrl('/search/article')
    return await http.get(url, data)
  },

}

export default searchService
