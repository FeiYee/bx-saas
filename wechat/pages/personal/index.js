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
      try {
        await home.getUserDetail()
      } catch (error) {
        this.getTabBar().showActionSheet();
      }
      let user = context.getUser();
      this.setData({title: user.username})
    } else {
      this.getTabBar().showActionSheet();
    }
  },

  onInformationClick() {
    let token = context.getToken();
    if (!token) {
      this.getTabBar().showActionSheet();
      return;
    }
    wx.navigateTo({
      url: '/pages/information/index',
    })
  }
})
