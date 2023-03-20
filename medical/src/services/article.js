import http from '../core/http.js'

const articleService = {
  prefix: '',
  getUrl(url) {
    return this.prefix + url
  },

  // async getArticles() {
  //   let url = this.getUrl(`/article`)
  //   return await http.get(url)
  // },

  // async getArticlesByTitle(title) {
  //   let data = {
  //     title
  //   }
  //   let url = this.getUrl(`/article/query`)
  //   return await http.get(url, data)
  // },



}

export default articleService
