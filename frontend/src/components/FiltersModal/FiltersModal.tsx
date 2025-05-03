import { Dispatch, SetStateAction, useState } from "react"
import { Modal } from "../../ui/Modal"
import styles from './FiltersModal.module.scss'
import { Button } from "../../ui/Button"
import CloseIcon from '@mui/icons-material/Close';
import { TextInput } from "../../ui/TextInput";


export interface FiltersModalProps {
  isOpen: boolean
  setIsOpen: Dispatch<SetStateAction<boolean>>
  data: any
  setData: any
}

export const FiltersModal = (props: FiltersModalProps) => {
  const {isOpen, setIsOpen, data, setData} = props

  const [datetime, setDatetime] = useState(data?.datetime || '')
  const [transactionType, setTransactionType] = useState(data?.transactionType || '')
  const [amount, setAmount] = useState(data?.amount || '')
  const [status, setStatus] = useState(data?.status || '')
  const [senderBank, setSenderBank] = useState(data?.senderBank || '')
  const [recipientBank, setRecipientBank] = useState(data?.recipientBank || '')
  const [recipientInn, setRecipientInn] = useState(data?.recipientInn || '')
  const [category, setCategory] = useState(data?.category || '')

  return (
    <Modal isOpen={isOpen}>
      <div className={styles.form}>
        <CloseIcon className={styles.close} onClick={() => setIsOpen(false)}/>
        <h1>Фильтры</h1>
        <div className={styles.wrap}>
          <TextInput className={styles.input} label="Дата и время операции" value={datetime} setValue={setDatetime}/>
          <TextInput className={styles.input} label="Тип транзакции" value={transactionType} setValue={setTransactionType}/>
          <TextInput className={styles.input} label="Сумма" value={amount} setValue={setAmount}/>
          <TextInput className={styles.input} label="Статус операции" value={status} setValue={setStatus}/>
          <TextInput className={styles.input} label="Банк отправителя" value={senderBank} setValue={setSenderBank}/>
          <TextInput className={styles.input} label="Банк получателя" value={recipientBank} setValue={setRecipientBank}/>
          <TextInput className={styles.input} label="ИНН получателя" value={recipientInn} setValue={setRecipientInn}/>
          <TextInput className={styles.input} label="Категория" value={category} setValue={setCategory}/>
        </div>
        <Button className={styles.add} onClick={() => { 
          setData({
            datetime,
            transactionType,
            amount,
            status,
            senderBank,
            recipientBank,
            recipientInn,
            category
          })
          setIsOpen(false)
        }}>Применить</Button>
      </div>
    </Modal>
  )
}