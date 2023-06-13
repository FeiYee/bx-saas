// index.js
Page({
  data: {
    checked: true,
    papers: [
      {
        title: '资料标题',
        desc: '资料描述信息',
        checked: false,
      },
      {
        title: '资料标题',
        desc: '资料描述信息',
        checked: false,
      },
      {
        title: '资料标题',
        desc: '资料描述信息',
        checked: false,
      },
      {
        title: '资料标题',
        desc: '资料描述信息',
        checked: false,
      },
      {
        title: '资料标题',
        desc: '资料描述信息',
        checked: false,
      }
    ],
    show: true,
    actions: [
      { name: '获取用户信息', color: '#07c160', openType: 'getUserInfo' },
      {
        name: '选项',
      },
      {
        name: '选项',
      },
      {
        name: '选项',
        subname: '描述信息',
        openType: 'share',
      },
    ],
  },

  onChange(event) {
    console.log(event)
    this.setData({
      checked: event.detail,
    });
  },
  getPhoneNumber (e) {
    console.log(e.detail.code)
  },
  onShow() {
    this.getTabBar().setActive();
  }
})
