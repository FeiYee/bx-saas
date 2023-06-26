// index.js
const context = require('../../common/context.js');
const home = require('../../services/home.js');

Page({
  data: {
    title: '未登录',
    desc: ''
  },
  async onShow() {
    this.getTabBar().setActive();
    let token = context.getToken();
    if (token) {
      await home.getUserDetail()
      let user = context.getUser();
      this.setData({title: user.username})
    } else {
      this.getTabBar().showActionSheet();
    }
  }
})
