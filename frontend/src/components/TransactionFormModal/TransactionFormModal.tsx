import { Modal } from "../../ui/Modal"
import CloseIcon from '@mui/icons-material/Close';
import styles from "./TransactionFormModal.module.scss"
import { Dispatch, SetStateAction, useEffect, useMemo, useState } from "react";
import { TextInput } from "../../ui/TextInput";
import { Button } from "../../ui/Button";
import { useAddTransaction } from "../../hooks/transaction/useAddTransaction";
import { useUpdateTransaction } from "../../hooks/transaction/useUpdateTransaction";
import { PartyType, Transaction, TransactionStatus, TransactionType } from "../../api/transaction.api";
import { Autocomplete } from "../../ui/Autocomplete";
import { IOption, PARTY_TYPE_OPTIONS, TRANSACTION_STATUS_OPTIONS, TRANSACTION_TYPE_OPTIONS } from "../../utils";
import { useGetTransactionsCategories } from "../../hooks/transaction/useGetCategories";
import { useGetBanks } from "../../hooks/bank/useGetBanks";

export type TTransactionFormMode = "view" | "add" | "edit" | undefined

export interface TransactionFormModalProps {
  mode: TTransactionFormMode
  setMode: Dispatch<SetStateAction<TTransactionFormMode>>
  defaultData?: Transaction
}

export const TransactionFormModal = (props: TransactionFormModalProps) => {
  const {mode, setMode, defaultData} = props

  const add = useAddTransaction()
  const update = useUpdateTransaction()

  const {data: banks} = useGetBanks()
  const {data: categories} = useGetTransactionsCategories()

  const [faceType, setFaceType] = useState<IOption<PartyType> | undefined>(PARTY_TYPE_OPTIONS.find(opt => opt.value === defaultData?.party_type))
  const [datetime, setDatetime] = useState(defaultData?.occurred_at || new Date().toISOString())
  const [transactionType, setTransactionType] = useState<IOption<TransactionType> | undefined>(TRANSACTION_TYPE_OPTIONS.find(opt => opt.value === defaultData?.transaction_type))
  const [comment, setComment] = useState(defaultData?.comment || '')
  const [amount, setAmount] = useState(defaultData?.amount || '')
  const [status, setStatus] = useState<IOption<TransactionStatus> | undefined>(TRANSACTION_STATUS_OPTIONS.find(opt => opt.value === defaultData?.status))
  const [senderBank, setSenderBank] = useState<IOption<number>>()
  const [check, setCheck] = useState(defaultData?.account_number || '')
  const [recipientBank, setRecipientBank] = useState<IOption<number>>()
  const [recipientInn, setRecipientInn] = useState(defaultData?.recipient_inn || '')
  const [recipientCurrentAccount, setRecipientCurrentAccaunt] = useState(defaultData?.recipient_account_number || '')
  const [category, setCategory] = useState<IOption<number>>()
  const [recipientPhone, setRecipientPhone] = useState(defaultData?.recipient_phone || '')

  useEffect(() => {
    if (!categories || !defaultData) { return }

    const category = categories.find(cat =>cat.value === defaultData.category_id)
    setCategory(category)
  }, [categories, defaultData])

  useEffect(() => {
    if (!banks || !defaultData) { return }

    const sBank = banks.find(bank => bank.value === defaultData.sender_bank_id)
    const rBank = banks.find(bank => bank.value === defaultData.recipient_bank_id)
  
    setSenderBank(sBank)
    setRecipientBank(rBank)
  }, [banks, defaultData])

  const title = useMemo(() => {
    if (mode === "add") {
      return "Создание транзакции"
    }
    if (mode === 'edit') {
      return "Редактирование транзакции"
    }
    return "Просмотр транзакции"
  }, [mode])

  return (
    <Modal isOpen={!!mode}>
      <div className={styles.form}>
        <CloseIcon className={styles.close} onClick={() => setMode(undefined)}/>
        <h1>{title}</h1>
        <div className={styles.wrap}>
          <Autocomplete disabled={mode === "view"} className={styles.input} label="Тип лица" options={PARTY_TYPE_OPTIONS} value={faceType} setValue={setFaceType}/>
          <TextInput disabled={mode === "view"} className={styles.input} label="Дата и время операции" value={datetime} setValue={setDatetime}/>
          <Autocomplete disabled={mode === "edit" || mode === 'view'} className={styles.input} label="Тип транзакции" options={TRANSACTION_TYPE_OPTIONS} value={transactionType} setValue={setTransactionType}/>
          <TextInput disabled={mode === "view"} className={styles.input} label="Комментарий к операции" value={comment} setValue={setComment}/>
          <TextInput disabled={mode === "view"} className={styles.input} label="Сумма" value={amount} setValue={setAmount}/>
          <Autocomplete disabled={mode === "view"} className={styles.input} label="Статус операции" options={TRANSACTION_STATUS_OPTIONS} value={status} setValue={setStatus}/>
          <Autocomplete disabled={mode === "view"} className={styles.input} label="Банк отправителя" options={banks || []} value={senderBank} setValue={setSenderBank}/>
          <TextInput disabled={mode === "edit" || mode === 'view'} className={styles.input} label="Счет поступления / списания" value={check} setValue={setCheck}/>
          <Autocomplete disabled={mode === "view"} className={styles.input} label="Банк получателя" options={banks || []} value={recipientBank} setValue={setRecipientBank}/>
          <TextInput disabled={mode === "view"} className={styles.input} label="ИНН получателя" value={recipientInn} setValue={setRecipientInn}/>
          <TextInput disabled={mode === "edit" || mode === 'view'} className={styles.input} label="Расчетный счет получателя" value={recipientCurrentAccount} setValue={setRecipientCurrentAccaunt}/>
          <Autocomplete disabled={mode === "view"} className={styles.input} label="Категория" options={categories || []} value={category} setValue={setCategory}/>
          <TextInput disabled={mode === "view"} className={styles.input} label="Телефон получателя" value={recipientPhone} setValue={setRecipientPhone}/>
        </div>
        <Button className={styles.add} onClick={() => { 
          if (
            !faceType ||
            !transactionType ||
            !senderBank ||
            !recipientBank ||
            !category ||
            !status
          ) {
            return;
          }
          if (mode === "add") {
            add.mutate({
              party_type: faceType.value,
              occurred_at: datetime,
              transaction_type: transactionType.value,
              comment,
              amount,
              status: status.value,
              sender_bank_id: senderBank.value,
              account_number: check,  
              recipient_bank_id: recipientBank.value,
              recipient_inn: recipientInn,
              recipient_account_number: recipientCurrentAccount,
              category_id: category.value,
              recipient_phone: recipientPhone,
            }, {
              onSuccess: () => {setMode(undefined)},
              onError: (e) => alert(JSON.stringify(e.response?.data, undefined, 2))
            })
            return;
          }
          if (mode === "edit" && defaultData) {
            update.mutate({
              id: defaultData.id,
              party_type: faceType.value,
              occurred_at: datetime,
              comment,
              amount,
              status: status.value,
              sender_bank_id: senderBank.value,
              recipient_bank_id: recipientBank.value,
              recipient_inn: recipientInn,
              category_id: category.value,
              recipient_phone: recipientPhone,
            }, {
              onSuccess: () => {setMode(undefined)},
              onError: (e) => alert(JSON.stringify(e.response?.data, undefined, 2))
            })
            return;
          }
          setMode(undefined)
        }}>{mode === "add" ? "Добавить" : mode === "edit" ? "Изменить" : "Закрыть"}</Button>
      </div>
    </Modal>
  )
}