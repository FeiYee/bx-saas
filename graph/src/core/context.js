
const tokenKey = 'token'
const userKey = 'user'
const keywordKey = 'keyword'
const topLevelKey = 'topLevel'


const setToken = function(token) {
  localStorage.setItem(tokenKey, token)
}

const getToken = function() {
  let token = localStorage.getItem(tokenKey)
  return token
}

const setUser = function(user) {
  let data = JSON.stringify(user)
  localStorage.setItem(userKey, data)
}

const getUser = function() {
  let user = localStorage.getItem(userKey)
  return JSON.parse(user)
}

const setKeyword = function(keyword) {
  localStorage.setItem(keywordKey, keyword)
}

const getKeyword = function() {
  let keyword = localStorage.getItem(keywordKey)
  return keyword
}

const setTopLevel = function(topLevel) {
  localStorage.setItem(topLevelKey, topLevel)
}

const getTopLevel = function() {
  let topLevel = localStorage.getItem(topLevelKey)
  topLevel = parseInt(topLevel || '0')
  return topLevel
}

export default {
  setToken,
  getToken,
  setUser,
  getUser,
  setKeyword,
  getKeyword,
  setTopLevel,
  getTopLevel,
}
