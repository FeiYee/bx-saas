// index.js
const context = require('../../common/context.js');
const userService = require('../../services/user.js');

Page({
  data: {
    birthdayShow: false,
    sexShow: false,
    minBirthday: new Date(1920, 10, 1).getTime(),
    maxBirthday: new Date().getTime(),
    birthdayValue: new Date().getTime(),
    sexList: ['男', '女'],
    birthday: new Date().getTime(),
    sex: '男',
    email: '',
    school: '',
    major: '',
    company: '',
  },
  async onShow() {
    const userInformation = context.getUserInformation();
    this.setData({
      birthday: userInformation.birthday,
    });
    this.setData({
      sex: userInformation.sex,
    });
    this.setData({
      email: userInformation.email,
    });
    this.setData({
      school: userInformation.school,
    });
    this.setData({
      major: userInformation.major,
    });
    this.setData({
      company: userInformation.company,
    });
  },
  onBirthdayClick() {
    this.setData({
      birthdayShow: true
    })
  },
  onBirthdayInput(event) {
    let date = this.formatter(event.detail);
    this.setData({
      birthday: date,
    });
  },
  onBirthdayCancel() {
    this.setData({
      birthdayShow: false
    })
  },
  onBirthdayConfirm() {
    this.setData({
      birthdayShow: false
    })
  },
  onSexClick() {
    this.setData({
      sexShow: true
    })
  },
  onSexChange(event) {
    const { picker, value, index } = event.detail;
    this.setData({
      sex: value
    })
  },
  onSexCancel() {
    this.setData({
      sexShow: false
    })
  },
  onSexConfirm() {
    this.setData({
      sexShow: false
    })
  },
  onEmailChange(event) {
    this.setData({
      email: event.detail
    });
  },
  onSchoolChange(event) {
    this.setData({
      school: event.detail
    });
  },
  onMajorChange(event) {
    this.setData({
      major: event.detail
    });
  },
  onCompanyChange(event) {
    this.setData({
      company: event.detail
    });
  },
  async onSave() {
    let user = {
      id: context.getUser().id || '53f3ff7fc205485483e98fdfca85b0f5',
      birthday: this.data.birthday,
      sex: this.data.sex,
      email: this.data.email,
      school: this.data.school,
      major: this.data.major,
      company: this.data.company,
    };
    try {
      await userService.updateUserInformation(user)
      wx.showToast({
        title: '保存成功',
      })
    } catch (error) {
      
    }
  },

  formatter(date) {
    let d = new Date(date)
    const year = d.getFullYear();
    const month = d.getMonth();
    const day = d.getDate();
    return `${year}-${month}-${day}`
  }

})
