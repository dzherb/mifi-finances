import axios, { AxiosInstance, AxiosResponse } from 'axios'


export const REFRESH = "refresh-token"
export const ACCESS = "access-token"

const URL = "http://localhost/api"

const instance = axios.create({
  baseURL: URL,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem(ACCESS)}`
  },
})

export async function withRetry(req: (inst: AxiosInstance) => Promise<AxiosResponse<any, any>>) {
  const axiosInstance = axios.create({
    baseURL: URL,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem(ACCESS)}`
    },
  })
  let res;
  try {
    res = await req(axiosInstance)
  } catch (e) {
    await getToken()
    axiosInstance.defaults.headers.common['Authorization'] = localStorage.getItem(ACCESS)
    res = await req(axiosInstance)
  }

  return res
}


export async function getToken(): Promise<void> {
  const res = await instance.post('user/refresh', {refresh: getCookie(REFRESH)})

  if (res.status === 401) {
    throw new Error("Unauthorized")
  }

  const {access, refresh} = res.data
  
  setCookie(REFRESH, refresh)
  localStorage.setItem(ACCESS, access)
}


export function getCookie(name: string) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

export function setCookie(name: string, value: string, options: Record<any, any> = {}) {
  options = {
    path: '/',
    // при необходимости добавьте другие значения по умолчанию
    ...options
  };

  if (options.expires instanceof Date) {
    options.expires = options.expires.toUTCString();
  }

  let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

  for (let optionKey in options) {
    updatedCookie += "; " + optionKey;
    let optionValue = options[optionKey];
    if (optionValue !== true) {
      updatedCookie += "=" + optionValue;
    }
  }

  document.cookie = updatedCookie;
}


export default instance