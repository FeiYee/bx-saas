
const tokenKey = 'token'
const userKey = 'user'

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

export default {
  setToken,
  getToken,
  setUser,
  getUser,
}
