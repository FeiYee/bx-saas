import http from '../core/http.js'

const articleExtractService = {
  prefix: '',
  getUrl(url) {
    return this.prefix + url
  },

  async getArticleExtracts(articleId) {
    let url = this.getUrl(`/article/${articleId}/extract`)
    return await http.get(url)
  },

}

export default articleExtractService
