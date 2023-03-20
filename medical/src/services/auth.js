import http from '../core/http.js'

const authService = {
  prefix: '',
  getUrl(url) {
    return this.prefix + url
  },

  async register(data) {
    let url = this.getUrl('/register')
    return await http.postFormUrlencoded(url, data)
  },

  async login(data) {
    let url = this.getUrl('/login')
    return await http.postFormUrlencoded(url, data)
  },

  async logout(data) {
    let url = this.getUrl('/logout')
    return await http.postFormUrlencoded(url, data)
  },

  async getUserDetail() {
    let url = this.getUrl('/user/detail')
    return await http.get(url)
  },

}

export default authService
