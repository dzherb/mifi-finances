import axios, { ACCESS, REFRESH, setCookie, withRetry } from './axios'
import { isMockApi } from './utils';


export async function getUser(): Promise<unknown> {
  if (isMockApi()) {
    return {}
  }

  try {
    const res = await withRetry(async (instance) => {return instance.get('/user')})
    const user = res.data
  
    return user
  } catch (err) {
    return;
  }
}


export async function createAccaunt(email: string, password: string): Promise<boolean> {
  if (isMockApi()) {
    return true
  }

  const res = await axios.post('user/accaunt/create', {email, password})
  return res.status === 200;
}


export async function login(email: string, password: string): Promise<boolean> {
  if (isMockApi()) {
    return true
  }

  const res = await axios.post('user/login', {email, password})

  const {access, refresh} = res.data
  setCookie(REFRESH, refresh)
  localStorage.setItem(ACCESS, access)

  return res.status === 200;
}


export async function logout(): Promise<boolean> {
  if (isMockApi()) {
    return true
  }

  const res = await withRetry(async (instance) => {return instance.post('user/logout')})
  setCookie(REFRESH, '')
  localStorage.setItem(ACCESS, '')

  return res.status === 200;
}
