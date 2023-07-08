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
  setUserInformation(userInformation) {
    wx.setStorageSync('userInformation', userInformation)
  },
  getUserInformation() {
    return wx.getStorageSync('userInformation')
  },
}

module.exports = context;