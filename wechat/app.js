// app.js
App({
  onLaunch (options) {
    // Do something initial when launch.
    wx.getUserProfile({
      desc: 'desc',
      success(res) {
        console.log(res)
      },
      fail(e) {
        console.log(e)
      }
    })
    wx.login({
      success: (res) => {
        console.log(res)
      },
      fail(e) {
        console.log(e)
      }
    })
  },
  onShow (options) {
    // Do something when show.
  },
  onHide () {
    // Do something when hide.
  },
  onError (msg) {
    console.log(msg)
  },
  globalData: 'I am global data'
})
