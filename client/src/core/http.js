import axios from 'axios'
import qs from 'qs'
import context from './context.js'
import {apiPrefix} from './config'

const instance = axios.create({
  baseURL: apiPrefix,
  timeout: 300000,
  headers: {
    'Authorization': `Bearer ${context.getToken()}`,
  }
});

instance.interceptors.request.use(function (config) {
  // 在发送请求之前做些什么
  config.headers.Authorization = `Bearer ${context.getToken()}`
  return config;
}, function (error) {
  // 对请求错误做些什么
  return Promise.reject(error);
});

// 添加响应拦截器
instance.interceptors.response.use(function (response) {
  // 2xx 范围内的状态码都会触发该函数。
  // 对响应数据做点什么
  return response;
}, function (error) {
  // 超出 2xx 范围的状态码都会触发该函数。
  // 对响应错误做点什么
  console.log(error)
  if (error.response.status === 403) {
    context.setToken('')
    window.location.href = '/'
  }

  return Promise.reject(error);
});



const request = {
  async get(url, params) {
    url = url + '?' + qs.stringify(params)
    try {
      let res = await instance.get(url, params)
      return res.data
    } catch (err) {
      throw err.response.data
    }
  },
  async post(url, params) {
    try {
      let res = await instance.post(url, params)
      return res.data
    } catch (err) {
      throw err.response.data
    }
  },
  async postFormData(url, params) {
    const config = {
      transformRequest: function (data, headers) {
        let formData = new FormData()
        Object.keys(data).forEach(key => {
          let value = data[key]
          formData.append(key, value)
        })
        return formData
      },
    }
    try {
      let res = await instance.post(url, params, config)
      return res.data
    } catch (err) {
      throw err.response.data
    }
  },
  async postFormUrlencoded(url, params) {
    const config = {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
      },
      transformRequest: function (data, headers) {
        return qs.stringify(data, {arrayFormat: 'brackets'})
      },
    }
    try {
      let res = await instance.post(url, params, config)
      return res.data
    } catch (err) {
      throw err.response.data
    }
  },
  async put(url, params) {
    try {
      let res = await instance.put(url, params)
      return res.data
    } catch (err) {
      throw err.response.data
    }
  },
  async patch(url, params) {
    try {
      let res = await instance.patch(url, params)
      return res.data
    } catch (err) {
      throw err.response.data
    }
  },
  async delete(url, params) {
    try {
      let res = await instance.delete(url, params)
      return res.data
    } catch (err) {
      throw err.response.data
    }
  },
}

export default request



