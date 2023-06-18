const config = require('../common/config');
const context = require('../common/context');


function login(code) {
  if (code) {
    wx.request({
      url: config.host + '/api/wechat/login',
      method: 'POST',
      data: {
        code: code,
        info: ''
      },
      success(res) {
        console.log(res)
        context.setToken(res)
      },
      fail(err) {
        wx.showToast({
          title: '等了失败',
        })
      }
    })
  }
}


function _login(code) {
  wx.login({
    success: (res) => {
      if (res.code) {
        wx.request({
          url: config.host + '/api/wechat/login',
          data: {
            code: res.code,
            info: ''
          },
          success(res) {
            console.log(res)
          },
          fail(err) {
            wx.showToast({
              title: '等了失败',
            })
          }
        })
      }
    },
  })
}

module.exports = login;
