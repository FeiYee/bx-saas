const context = {
  setToken(token) {
    wx.setStorageSync('token', token)
  },
  getToken() {
    return wx.getStorageSync('token')
  },
  setUser(user) {
    wx.setStorageSync('user', user)
  },
  getUser() {
    return wx.getStorageSync('user')
  },
}

module.exports = context;