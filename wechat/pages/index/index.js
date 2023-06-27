// index.js
const context = require('../../common/context.js');
const home = require('../../services/home.js');

Page({
  async onShow() {
    this.getTabBar().setActive();
    let token = context.getToken();
    if (token) {
      try {
        await home.getUserDetail()
      } catch (error) {
        this.getTabBar().showActionSheet();
      }
    } else {
      this.getTabBar().showActionSheet();
    }
  }
})
