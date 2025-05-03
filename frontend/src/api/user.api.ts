import axios, { ACCESS, getToken, REFRESH, setCookie, withRetry } from './axios'
import { isMockApi } from './utils';


export async function checkAuth(): Promise<boolean> {
  if (isMockApi()) {
    return true
  }

  try {
    await getToken();
    return true;
  } catch (err) {
    return false;
  }
}


export async function createAccaunt(email: string, password: string): Promise<boolean> {
  if (isMockApi()) {
    return true
  }

  const res = await axios.post('/auth/register', {username: email, password})
  return res.status === 201;
}


export async function login(email: string, password: string): Promise<boolean> {
  if (isMockApi()) {
    return true
  }

  const res = await axios.post('auth/login', {username: email, password})

  const {access_token: access, refresh_token: refresh} = res.data
  setCookie(REFRESH, refresh)
  localStorage.setItem(ACCESS, access)

  return res.status === 200;
}


export async function logout(): Promise<boolean> {
  if (isMockApi()) {
    return true
  }

  const res = await withRetry(async (instance) => {return instance.post('auth/logout')})
  setCookie(REFRESH, '')
  localStorage.setItem(ACCESS, '')

  return res.status === 200;
}
