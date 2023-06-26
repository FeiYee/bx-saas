// index.js
const context = require('../../common/context.js');
const home = require('../../services/home.js');

Page({
  onShow() {
    this.getTabBar().setActive();
    let token = context.getToken();
    if (token) {
      home.getUserDetail()
    } else {
      this.getTabBar().showActionSheet();
    }
  }
})
