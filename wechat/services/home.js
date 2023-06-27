const config = require('../common/config');
const context = require('../common/context');

function getUserDetail() {
  return new Promise((resolve, reject) => {
    wx.request({
      url: config.host + '/api/user/detail',
      method: 'GET',
      header: {
        Authorization: `Bearer ${context.getToken()}`
      },
      data: {
      },
      success(res) {
        console.log(res)
        if (res.statusCode === 200) {
          let user = res.data.user;
          context.setUser(user);
          resolve(user);
        } else {
          reject(res.data);
        }
      },
      fail(err) {
        reject(err);
        wx.showToast({
          title: '获取用户信息失败' + JSON.stringify(err),
        })
      }
    })
  });
    
}

module.exports = {
  getUserDetail
};
