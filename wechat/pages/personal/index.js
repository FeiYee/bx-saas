// index.js
Page({
  data: {
    title: '未登录',
    desc: ''
  },
  onShow() {
    this.getTabBar().setActive();
    this.getTabBar().showActionSheet()
  }
})
