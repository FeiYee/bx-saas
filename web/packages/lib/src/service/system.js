import http from '../core/http.js'

const systemService = {
  prefix: '',
  getUrl(url) {
    return this.prefix + url
  },

  async getUsers(data) {
    let url = this.getUrl('/user')
    return await http.get(url, data)
  },
  async createUser(data) {
    let url = this.getUrl('/user')
    return await http.post(url, data)
  },
  async updateUser(data) {
    let id = data.id
    let url = this.getUrl(`/user/${id}`)
    return await http.put(url, data)
  },
  async deleteUser(id) {
    let url = this.getUrl(`/user/${id}`)
    return await http.delete(url)
  },

  async getOrgs(data) {
    let url = this.getUrl('/org')
    return await http.get(url, data)
  },
  async createOrg(data) {
    let url = this.getUrl('/org')
    return await http.post(url, data)
  },
  async updateOrg(data) {
    let id = data.id
    let url = this.getUrl(`/org/${id}`)
    return await http.put(url, data)
  },
  async deleteOrg(id) {
    let url = this.getUrl(`/org/${id}`)
    return await http.delete(url)
  },

  async getOrgUsers(data) {
    let id = data.id
    let url = this.getUrl(`/org/${id}/user`)
    return await http.get(url, data)
  },

  async createOrgUser(orgId, userIdList) {
    let data = userIdList

    let url = this.getUrl(`/org/${orgId}/user`)
    return await http.post(url, data)
  },

}

export default systemService
