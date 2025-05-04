import { withRetry } from "./axios"

export interface Transaction {
  id: number
  party_type: PartyType
  occurred_at: string
  transaction_type: TransactionType
  comment: string
  amount: string
  status: TransactionStatus
  sender_bank_id: number
  account_number: string
  recipient_bank_id: number
  recipient_inn: string
  recipient_account_number: string
  category_id: number
  recipient_phone: string
}
export type PartyType = "INDIVIDUAL" | "LEGAL_ENTITY"
export type TransactionType = "CREDIT" | "DEBIT"
export type TransactionStatus = "NEW" | "CONFIRMED" | "PROCESSING" | "CANCELLED" | "EXECUTED" | "DELETED" | "REFUNDED"

export interface TransactionCategory {
  name: string
  id: number
}


export interface GetTransactionsReq {
  offset: number
  limit: number
  order_by?: string
}
export async function getTransactions(options: GetTransactionsReq): Promise<Transaction[]> {
    const res = await withRetry(async (instance) => {return instance.get('/transactions', {params: options})})
  
    if (res.status === 200) {
      return res.data
    }
  
    return []
}


export type AddTransactionReq = Omit<Transaction, "id">
export async function addTransaction(options: AddTransactionReq) {
  const res = await withRetry(async (instance) => {return instance.post('/transactions', options)})
  return res.status === 201
}

export type UpdateTransactionReq = Omit<Transaction, "id" | "transaction_type" | "account_number" | "recipient_account_number"> & {id?: number}
export async function updateTransaction(options: UpdateTransactionReq) {
  const id = options.id
  delete options.id
  
  const res = await withRetry(async (instance) => {return instance.patch(`/transactions/${id}`, options)})
  return res.status === 200
}

export async function getTransactionsCategories(): Promise<TransactionCategory[]> {
  const res = await withRetry(async (instance) => {return instance.get('/transactions/categories')})
  
  if (res.status === 200) {
    return res.data
  }

  return []
}

export async function createTransactionCategory(name: string) {
  const res = await withRetry(async (instance) => {return instance.post('/transactions/categories', {name})})
  return res.status === 201
}

export async function deleteTransactionCategory(id: string) {
  const res = await withRetry(async (instance) => {return instance.delete(`/transactions/categories/${id}`)})
  return res.status === 204
}