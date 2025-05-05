import { withRetry } from "./axios"


export interface IBank {
  name: string
  id: number
}

export async function getBanks(): Promise<IBank[]> {
  const res = await withRetry(async (instance) => {return instance.get('/banks')})

  if (res.status === 200) {
    return res.data
  }

  return []
}

export async function addBank(name: string): Promise<boolean> {
  const res = await withRetry(async (instance) => {return instance.post('/banks', {name})})
  return res.status === 201
}

export async function deleteBank(id: string): Promise<boolean> {
  const res = await withRetry(async (instance) => {return instance.delete(`/banks/${id}`)})
  return res.status === 204
}