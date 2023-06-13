const context = {
  setToken(token) {
    wx.setStorageSync('token', token)
  },
  getToken() {
    return wx.getStorageSync('token')
  },
}

module.exports = context;