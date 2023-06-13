// index.js
Page({
  data: {
    active: 0,
    tabs: [
      {
        pagePath: "/pages/index/index",
        text: "首页",
        icon: "wap-home-o"
      },
      // {
      //   pagePath: "/pages/paper/index",
      //   text: "资料",
      //   icon: "star-o"
      // },
      // {
      //   pagePath: "/pages/login/index",
      //   text: "设置",
      //   icon: "setting-o"
      // },
      {
        pagePath: "/pages/personal/index",
        text: "我的",
        icon: "user-circle-o"
      }
    ],
    isActionShow: false,
    actions: [
      // { name: '同意并授权', subname: '获取您的昵称、头像', color: '#07c160', openType: 'getUserInfo' },
      { name: '同意并授权', subname: '绑定微信手机号', color: '#07c160', openType: 'getPhoneNumber' },
    ],
  },
  setActive() {
    const page = getCurrentPages().pop();
    const index = this.data.tabs.findIndex(item => item.pagePath === `/${page.route}`);
    this.setData({ active: index });
  },
  onChange(event) {
    // event.detail 的值为当前选中项的索引
    // this.setData({ active: event.detail });
    wx.switchTab({
      url: this.data.tabs[event.detail].pagePath,
    });
  },

  showActionSheet() {
    this.setData({ isActionShow: true });
  },
  onClose() {
    this.setData({ isActionShow: false });
  },
  onGetUserInfo(e) {
    console.log(e.detail);
  },
  onGetPhoneNumber(e) {
    console.log(e.detail);

  }
})
