import { PartyType, TransactionStatus, TransactionType } from "../api/transaction.api";
import { IOption } from "./types";


export const PARTY_TYPE_OPTIONS: IOption<PartyType>[] = [
  {
    value: "INDIVIDUAL",
    label: "INDIVIDUAL"
  },
  {
    value: "LEGAL_ENTITY",
    label: "LEGAL_ENTITY"
  }
]

export const TRANSACTION_TYPE_OPTIONS: IOption<TransactionType>[] = [
  {
    value: "CREDIT",
    label: "credit"
  },
  {
    value: "DEBIT",
    label: "debit"
  }
]

export const TRANSACTION_STATUS_OPTIONS: IOption<TransactionStatus>[] = [
  {
    value: "CANCELLED",
    label: "cancelled"
  },
  {
    value: "CONFIRMED",
    label: "confirmed"
  },
  {
    value: "DELETED",
    label: 'deleted'
  },
  {
    value: "EXECUTED",
    label: 'executed'
  },
  {
    value: "NEW",
    label: 'new'
  },
  {
    value: "PROCESSING",
    label: "processing"
  },
  {
    value: "REFUNDED",
    label: 'refunded'
  }
]
