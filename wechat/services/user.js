const config = require('../common/config');
const context = require('../common/context');

function updateUserInformation(user) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: config.host + '/api/user/information',
      method: 'POST',
      header: {
        Authorization: `Bearer ${context.getToken()}`
      },
      data: user,
      success(res) {
        console.log(res)
        if (res.statusCode === 200) {
          let user = res.data;
          context.setUserInformation(user);
          resolve(user);
        } else {
          reject(res.data);
        }
      },
      fail(err) {
        reject(err);
        wx.showToast({
          title: '更新用户信息失败' + JSON.stringify(err),
        })
      }
    })
  });
    
}

module.exports = {
  updateUserInformation
};
