import { Modal } from "../../ui/Modal"
import CloseIcon from '@mui/icons-material/Close';
import styles from "./TransactionFormModal.module.scss"
import { Dispatch, SetStateAction, useMemo, useState } from "react";
import { TextInput } from "../../ui/TextInput";
import { Button } from "../../ui/Button";

export type TTransactionFormMode = "view" | "add" | "edit" | undefined

export interface TransactionFormModalProps {
  mode: TTransactionFormMode
  setMode: Dispatch<SetStateAction<TTransactionFormMode>>
  defaultData?: any
}

export const TransactionFormModal = (props: TransactionFormModalProps) => {
  const {mode, setMode, defaultData} = props

  const [faceType, setFaceType] = useState(defaultData?.faceType || '')
  const [datetime, setDatetime] = useState(defaultData?.datetime || '')
  const [transactionType, setTransactionType] = useState(defaultData?.transactionType || '')
  const [comment, setComment] = useState(defaultData?.comment || '')
  const [amount, setAmount] = useState(defaultData?.amount || '')
  const [status, setStatus] = useState(defaultData?.status || '')
  const [senderBank, setSenderBank] = useState(defaultData?.senderBank || '')
  const [check, setCheck] = useState(defaultData?.check || '')
  const [recipientBank, setRecipientBank] = useState(defaultData?.recipientBank || '')
  const [recipientInn, setRecipientInn] = useState(defaultData?.recipientInn || '')
  const [recipientCurrentAccount, setRecipientCurrentAccaunt] = useState(defaultData?.recipientCurrentAccount || '')
  const [category, setCategory] = useState(defaultData?.category || '')
  const [recipientPhone, setRecipientPhone] = useState(defaultData?.recipientPhone || '')

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
          <TextInput disabled={mode === "view"} className={styles.input} label="Тип лица" value={faceType} setValue={setFaceType}/>
          <TextInput disabled={mode === "view"} className={styles.input} label="Дата и время операции" value={datetime} setValue={setDatetime}/>
          <TextInput disabled={mode === "edit" || mode === 'view'} className={styles.input} label="Тип транзакции" value={transactionType} setValue={setTransactionType}/>
          <TextInput disabled={mode === "view"} className={styles.input} label="Комментарий к операции" value={comment} setValue={setComment}/>
          <TextInput disabled={mode === "view"} className={styles.input} label="Сумма" value={amount} setValue={setAmount}/>
          <TextInput disabled={mode === "view"} className={styles.input} label="Статус операции" value={status} setValue={setStatus}/>
          <TextInput disabled={mode === "view"} className={styles.input} label="Банк отправителя" value={senderBank} setValue={setSenderBank}/>
          <TextInput disabled={mode === "edit" || mode === 'view'} className={styles.input} label="Счет поступления / списания" value={check} setValue={setCheck}/>
          <TextInput disabled={mode === "view"} className={styles.input} label="Банк получателя" value={recipientBank} setValue={setRecipientBank}/>
          <TextInput disabled={mode === "view"} className={styles.input} label="ИНН получателя" value={recipientInn} setValue={setRecipientInn}/>
          <TextInput disabled={mode === "edit" || mode === 'view'} className={styles.input} label="Расчетный счет получателя" value={recipientCurrentAccount} setValue={setRecipientCurrentAccaunt}/>
          <TextInput disabled={mode === "view"} className={styles.input} label="Категория" value={category} setValue={setCategory}/>
          <TextInput disabled={mode === "view"} className={styles.input} label="Телефон получателя" value={recipientPhone} setValue={setRecipientPhone}/>
        </div>
        <Button className={styles.add} onClick={() => { 
          /* TODO */
          setMode(undefined)
        }}>{mode === "add" ? "Добавить" : mode === "edit" ? "Изменить" : "Закрыть"}</Button>
      </div>
    </Modal>
  )
}